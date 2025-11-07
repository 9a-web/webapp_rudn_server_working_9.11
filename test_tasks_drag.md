# Тест перетаскивания задач в карточке "Сегодня"

## Проверочный список

### 1. Структура данных
- [ ] Каждая задача имеет уникальный `id`
- [ ] `todayTasks` это массив объектов задач
- [ ] Задачи передаются как `values` в Reorder.Group

### 2. Компоненты Framer Motion
- [x] Импортирован `Reorder` и `useDragControls`
- [x] `Reorder.Group` обернут вокруг списка задач
- [x] `Reorder.Item` используется для каждой задачи
- [x] `dragControls` создается через `useDragControls()`

### 3. Конфигурация Reorder.Item
- [x] `value={task}` - передан объект задачи
- [x] `dragListener={false}` - отключен автоматический слушатель
- [x] `dragControls={dragControls}` - передан контроллер
- [x] Нет дублирующего `key` атрибута внутри компонента

### 4. Drag Handle
- [x] `onPointerDown` с вызовом `dragControls.start(e)`
- [x] `e.stopPropagation()` для предотвращения конфликтов
- [x] `touchAction: 'none'` в style
- [x] `touch-none` и `select-none` классы

### 5. Стили и классы
- [x] Убран `overflow-y-auto` с родительского контейнера
- [x] `list-none` на Reorder.Group
- [x] `listStyle: 'none'` на Reorder.Item
- [x] `mb-2` для spacing между элементами

### 6. Callback функция
- [x] `onReorder={handleReorderTasks}` на Reorder.Group
- [x] `handleReorderTasks` правильно обновляет состояние

## Возможные проблемы

### Если перетаскивание не работает:

1. **Проверить в DevTools:**
   ```javascript
   // В консоли браузера
   console.log('Tasks:', todayTasks);
   console.log('Each task has id:', todayTasks.every(t => t.id));
   ```

2. **CSS конфликты:**
   - Проверить, нет ли `pointer-events: none` на родительских элементах
   - Убедиться, что нет `overflow: hidden` выше по иерархии
   - Проверить z-index элементов

3. **Event listeners:**
   - Убедиться, что нет других `onClick` или `onPointerDown` на родительских элементах
   - Проверить, что не используется `preventDefault()` где-то выше

4. **Framer Motion version:**
   - Убедиться, что версия >= 10.0.0
   - Проверить: `grep framer-motion package.json`

## Тестирование

### Вручную:
1. Открыть раздел "Список дел"
2. Найти карточку "Сегодня"
3. Нажать и удерживать иконку из 3 полосок (GripVertical)
4. Переместить задачу вверх или вниз
5. Отпустить - задача должна остаться на новом месте

### Что должно происходить:
- ✅ Haptic feedback при начале перетаскивания
- ✅ Курсор меняется на `grabbing`
- ✅ Задача следует за курсором/пальцем
- ✅ Другие задачи сдвигаются, освобождая место
- ✅ После отпускания задача остается на новом месте
- ✅ Порядок сохраняется в состоянии

## Отладка

### Console logs для проверки:
```javascript
// Добавить в handleReorderTasks
console.log('Reorder triggered', {
  oldOrder: todayTasks.map(t => t.id),
  newOrder: newOrder.map(t => t.id)
});
```

### Проверка dragControls:
```javascript
// В TodayTaskItem
console.log('Drag start', task.id);
```

### Проверка события:
```javascript
// В onPointerDown
console.log('Pointer down on task:', task.id, e);
```
