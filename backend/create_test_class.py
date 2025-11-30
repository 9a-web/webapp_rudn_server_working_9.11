
import asyncio
import os
import logging
from datetime import datetime, timedelta
import pytz
from motor.motor_asyncio import AsyncIOMotorClient
from scheduler_v2 import get_scheduler_v2
from dotenv import load_dotenv
from pathlib import Path

# Загрузка .env
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017/rudn_schedule")
# Используйте ваш Telegram ID для теста, если знаете. Или скрипт найдет первого попавшегося с уведомлениями.
TELEGRAM_ID = 765963392 
MOSCOW_TZ = pytz.timezone('Europe/Moscow')

async def create_test_class_6min():
    client = AsyncIOMotorClient(MONGO_URL)
    db_name = os.environ.get("DB_NAME", "rudn_schedule")
    db = client[db_name]
    
    now_msk = datetime.now(MOSCOW_TZ)
    today_str = now_msk.strftime('%Y-%m-%d')
    
    # День недели на русском
    current_day = now_msk.strftime('%A')
    day_mapping = {
        'Monday': 'Понедельник', 'Tuesday': 'Вторник', 'Wednesday': 'Среда',
        'Thursday': 'Четверг', 'Friday': 'Пятница', 'Saturday': 'Суббота', 'Sunday': 'Воскресенье'
    }
    russian_day = day_mapping.get(current_day, current_day)
    
    logger.info(f"🕒 Сейчас: {now_msk.strftime('%H:%M:%S')}")
    
    # 1. Настраиваем пользователя (ставим уведомление за 5 минут)
    # Если пара через 6 мин, а уведомление за 10 мин -> время уведомления (пара - 10) = 4 минуты назад. Пропуск.
    # Если пара через 6 мин, а уведомление за 5 мин -> время уведомления (пара - 5) = через 1 минуту. УСПЕХ.
    
    logger.info("⚙️ Устанавливаем время уведомления: 5 минут")
    await db.user_settings.update_one(
        {"telegram_id": TELEGRAM_ID},
        {"$set": {
            "notifications_enabled": True,
            "notification_time": 5, 
            "group_id": "TEST_GROUP_6MIN"
        }},
        upsert=True
    )

    # 2. Создаем пару через 6 минут
    class_time = now_msk + timedelta(minutes=6)
    start_time_str = class_time.strftime("%H:%M")
    # Конец через 1.5 часа
    end_time_str = (class_time + timedelta(minutes=90)).strftime("%H:%M")
    time_str = f"{start_time_str} - {end_time_str}"
    
    # Ожидаемое время отправки уведомления
    notification_time = class_time - timedelta(minutes=5)
    
    logger.info(f"🎓 Создаем пару на: {start_time_str} (через 6 минут)")
    logger.info(f"🔔 Ожидаемое время уведомления: {notification_time.strftime('%H:%M:%S')} (через 1 минуту)")

    fake_schedule = {
        "group_id": "TEST_GROUP_6MIN",
        "week_number": 1, # Пишем в обе недели для надежности
        "expires_at": datetime.utcnow() + timedelta(hours=1),
        "events": [
            {
                "day": russian_day,
                "discipline": "TEST: ПАРА ЧЕРЕЗ 6 МИНУТ",
                "time": time_str,
                "teacher": "Test Teacher",
                "auditory": "Room 666",
                "lessonType": "Эксперимент"
            }
        ]
    }

    # Обновляем кэш для обеих недель
    await db.schedule_cache.update_one({"group_id": "TEST_GROUP_6MIN", "week_number": 1}, {"$set": fake_schedule}, upsert=True)
    fake_schedule["week_number"] = 2
    await db.schedule_cache.update_one({"group_id": "TEST_GROUP_6MIN", "week_number": 2}, {"$set": fake_schedule}, upsert=True)
    
    logger.info("✅ Кэш расписания обновлен")

    # 3. Запускаем планировщик
    logger.info("🔄 Запускаем пересчет уведомлений...")
    scheduler = get_scheduler_v2(db)
    result = await scheduler.schedule_user_notifications(TELEGRAM_ID)
    
    logger.info(f"📊 Результат планирования: {result}")
    
    # 4. Проверяем, что попало в БД
    notification = await db.scheduled_notifications.find_one({
        "telegram_id": TELEGRAM_ID,
        "date": today_str,
        "class_info.discipline": "TEST: ПАРА ЧЕРЕЗ 6 МИНУТ"
    })
    
    if notification:
        status = notification['status']
        scheduled_at = notification['scheduled_time']
        # scheduled_time в БД хранится как naive datetime (UTC или Local? В scheduler_v2 мы делали notification_datetime.replace(tzinfo=None))
        # notification_datetime вычислялся от now (MOSCOW_TZ). Значит это московское время без зоны.
        
        logger.info(f"🎉 УСПЕХ! Уведомление найдено:")
        logger.info(f"   - Время отправки: {scheduled_at}")
        logger.info(f"   - Статус: {status}")
        
        if status == 'pending':
            logger.info("   ✅ Уведомление ожидает отправки!")
        else:
            logger.warning(f"   ⚠️ Статус не pending: {status}")
    else:
        logger.error("❌ ПРОВАЛ! Уведомление не создано.")

if __name__ == "__main__":
    asyncio.run(create_test_class_6min())
