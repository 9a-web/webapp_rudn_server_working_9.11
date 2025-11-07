/**
 * Контекст для Telegram WebApp
 * Предоставляет доступ к данным пользователя Telegram и функциям WebApp API
 */

import React, { createContext, useContext, useEffect, useState } from 'react';

const TelegramContext = createContext(null);

export const useTelegram = () => {
  const context = useContext(TelegramContext);
  if (!context) {
    throw new Error('useTelegram must be used within TelegramProvider');
  }
  return context;
};

export const TelegramProvider = ({ children }) => {
  const [webApp, setWebApp] = useState(null);
  const [user, setUser] = useState(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    // Инициализация Telegram WebApp
    if (typeof window !== 'undefined' && window.Telegram?.WebApp) {
      const tg = window.Telegram.WebApp;
      
      // 1. Сначала готовим WebApp
      tg.ready();
      
      // 2. ⭐️ ПОЛНОЭКРАННЫЙ РЕЖИМ - расширяем на весь экран
      // Это основной метод для Full Screen в Telegram Web App
      tg.expand();
      
      // 3. Проверяем, что expand сработал и повторяем при необходимости
      const ensureExpanded = () => {
        if (!tg.isExpanded) {
          console.log('⚠️ WebApp не развернут, повторная попытка expand()...');
          tg.expand();
        } else {
          console.log('✅ WebApp успешно развернут на весь экран');
        }
      };
      
      // Проверяем после небольшой задержки (Telegram API может работать асинхронно)
      setTimeout(ensureExpanded, 50);
      setTimeout(ensureExpanded, 200);
      setTimeout(ensureExpanded, 500);
      
      // 4. Отключаем вертикальные свайпы (предотвращает случайное закрытие)
      if (typeof tg.disableVerticalSwipes === 'function') {
        tg.disableVerticalSwipes();
        console.log('✅ Вертикальные свайпы отключены');
      }
      
      // 5. Включаем подтверждение закрытия (дополнительная защита)
      if (typeof tg.enableClosingConfirmation === 'function') {
        tg.enableClosingConfirmation();
        console.log('✅ Подтверждение закрытия включено');
      }
      
      // 6. Устанавливаем цвета темы для нативного вида
      if (typeof tg.setHeaderColor === 'function') {
        tg.setHeaderColor('#1C1C1E');
      }
      if (typeof tg.setBackgroundColor === 'function') {
        tg.setBackgroundColor('#1C1C1E');
      }
      
      // 7. Устанавливаем цвет bottom bar (если поддерживается)
      if (typeof tg.setBottomBarColor === 'function') {
        tg.setBottomBarColor('#1C1C1E');
      }
      
      // 8. Устанавливаем viewport meta для мобильных устройств
      const viewportMeta = document.querySelector('meta[name="viewport"]');
      if (viewportMeta) {
        viewportMeta.setAttribute('content', 
          'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover'
        );
      }
      
      // 9. Устанавливаем CSS переменные для полной высоты (учитывая Telegram UI)
      // Telegram Web App предоставляет viewportHeight для корректной работы
      if (tg.viewportHeight) {
        document.documentElement.style.setProperty('--tg-viewport-height', `${tg.viewportHeight}px`);
        document.documentElement.style.setProperty('--tg-viewport-stable-height', `${tg.viewportStableHeight || tg.viewportHeight}px`);
      }
      
      // 10. Слушаем изменения viewport (при открытии клавиатуры и т.д.)
      const handleViewportChanged = () => {
        if (tg.viewportHeight) {
          document.documentElement.style.setProperty('--tg-viewport-height', `${tg.viewportHeight}px`);
          document.documentElement.style.setProperty('--tg-viewport-stable-height', `${tg.viewportStableHeight || tg.viewportHeight}px`);
          console.log(`📐 Viewport изменен: ${tg.viewportHeight}px`);
        }
      };
      
      // Подписываемся на события изменения viewport
      tg.onEvent('viewportChanged', handleViewportChanged);
      
      // Получаем данные пользователя
      const userData = tg.initDataUnsafe?.user;
      
      setWebApp(tg);
      
      // Если пользователь есть - используем его, иначе mock данные
      if (userData) {
        setUser(userData);
      } else {
        // Mock данные для разработки вне Telegram
        console.warn('⚠️ Telegram user not found. Using mock data for development.');
        setUser({
          id: 123456789,
          first_name: 'Test',
          last_name: 'User',
          username: 'testuser',
        });
      }
      
      setIsReady(true);

      console.log('🚀 Telegram WebApp initialized:', {
        platform: tg.platform,
        version: tg.version,
        isExpanded: tg.isExpanded,
        viewportHeight: tg.viewportHeight,
        viewportStableHeight: tg.viewportStableHeight,
        user: userData || 'mock',
      });
      
      // Cleanup при размонтировании
      return () => {
        tg.offEvent('viewportChanged', handleViewportChanged);
      };
    } else {
      // Для разработки вне Telegram - используем mock данные
      console.warn('⚠️ Telegram WebApp не доступен. Используются mock данные для разработки.');
      setUser({
        id: 123456789,
        first_name: 'Test',
        last_name: 'User',
        username: 'testuser',
      });
      setIsReady(true);
    }
  }, []);

  const showAlert = (message) => {
    if (webApp) {
      webApp.showAlert(message);
    } else {
      alert(message);
    }
  };

  const showConfirm = (message) => {
    return new Promise((resolve) => {
      if (webApp) {
        webApp.showConfirm(message, resolve);
      } else {
        resolve(window.confirm(message));
      }
    });
  };

  const showPopup = (params) => {
    return new Promise((resolve) => {
      if (webApp) {
        webApp.showPopup(params, resolve);
      } else {
        alert(params.message);
        resolve(null);
      }
    });
  };

  const close = () => {
    if (webApp) {
      webApp.close();
    }
  };

  const sendData = (data) => {
    if (webApp) {
      webApp.sendData(JSON.stringify(data));
    }
  };

  const openLink = (url, options = {}) => {
    if (webApp) {
      webApp.openLink(url, options);
    } else {
      window.open(url, '_blank');
    }
  };

  const hapticFeedback = (type = 'impact', style = 'medium') => {
    if (webApp?.HapticFeedback) {
      if (type === 'impact') {
        webApp.HapticFeedback.impactOccurred(style);
      } else if (type === 'notification') {
        webApp.HapticFeedback.notificationOccurred(style);
      } else if (type === 'selection') {
        webApp.HapticFeedback.selectionChanged();
      }
    }
  };

  const value = {
    webApp,
    user,
    isReady,
    showAlert,
    showConfirm,
    showPopup,
    close,
    sendData,
    openLink,
    hapticFeedback,
  };

  return (
    <TelegramContext.Provider value={value}>
      {children}
    </TelegramContext.Provider>
  );
};

export default TelegramContext;
