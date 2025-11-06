import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { ClipboardList, Check } from 'lucide-react';

export const TasksSection = () => {
  // Временные данные для демонстрации
  const [todayTasks, setTodayTasks] = useState([
    { id: 1, text: 'Подготовка к экзамену', completed: false },
    { id: 2, text: 'Сдать лабораторную', completed: true },
    { id: 3, text: 'Домашнее задание', completed: false },
    { id: 4, text: 'Купить учебники', completed: false },
  ]);

  const toggleTask = (taskId) => {
    setTodayTasks(tasks => 
      tasks.map(task => 
        task.id === taskId ? { ...task, completed: !task.completed } : task
      )
    );
  };

  const currentDate = new Date().toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long'
  });

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
      className="min-h-[calc(100vh-140px)] bg-white rounded-t-[40px] mt-6 p-6"
    >
      {/* Header секции */}
      <div className="flex items-center gap-3 mb-6">
        <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-yellow-400 to-orange-400 flex items-center justify-center">
          <ClipboardList className="w-6 h-6 text-white" strokeWidth={2.5} />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-[#1C1C1E]">Список дел</h2>
          <p className="text-sm text-[#999999]">Управляйте своими задачами</p>
        </div>
      </div>

      {/* Карточка с задачами на сегодня */}
      <div className="flex gap-4">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="w-[160px] h-[200px] rounded-3xl bg-gradient-to-br from-yellow-50 to-orange-50 border border-yellow-200/50 p-4 flex flex-col"
          style={{
            boxShadow: '0 4px 16px rgba(251, 191, 36, 0.1)'
          }}
        >
          {/* Заголовок карточки */}
          <div className="mb-3">
            <h3 className="text-sm font-bold text-[#1C1C1E]">Сегодня</h3>
            <p className="text-xs text-[#999999] mt-0.5">{currentDate}</p>
          </div>

          {/* Список задач */}
          <div className="flex-1 overflow-y-auto space-y-2 scrollbar-thin scrollbar-thumb-yellow-300 scrollbar-track-transparent">
            {todayTasks.map((task) => (
              <motion.div
                key={task.id}
                whileTap={{ scale: 0.98 }}
                onClick={() => toggleTask(task.id)}
                className="flex items-start gap-2 cursor-pointer group"
              >
                {/* Checkbox */}
                <div 
                  className={`
                    w-4 h-4 rounded-md flex-shrink-0 flex items-center justify-center transition-all duration-200 mt-0.5
                    ${task.completed 
                      ? 'bg-gradient-to-br from-yellow-400 to-orange-400' 
                      : 'bg-white border-2 border-[#E5E5E5] group-hover:border-yellow-400'
                    }
                  `}
                >
                  {task.completed && (
                    <Check className="w-3 h-3 text-white" strokeWidth={3} />
                  )}
                </div>

                {/* Текст задачи */}
                <span 
                  className={`
                    text-xs leading-tight transition-all duration-200
                    ${task.completed 
                      ? 'text-[#999999] line-through' 
                      : 'text-[#1C1C1E] group-hover:text-yellow-600'
                    }
                  `}
                >
                  {task.text}
                </span>
              </motion.div>
            ))}
          </div>

          {/* Счетчик выполненных задач */}
          <div className="mt-3 pt-3 border-t border-yellow-200/30">
            <p className="text-xs text-[#999999] text-center">
              {todayTasks.filter(t => t.completed).length} / {todayTasks.length} выполнено
            </p>
          </div>
        </motion.div>

        {/* Placeholder для остального контента справа */}
        <div className="flex-1 flex flex-col items-center justify-center py-16">
          <div className="w-24 h-24 rounded-full bg-gradient-to-br from-yellow-400/10 to-orange-400/10 flex items-center justify-center mb-4">
            <ClipboardList className="w-12 h-12 text-yellow-500" strokeWidth={2} />
          </div>
          <h3 className="text-lg font-semibold text-[#1C1C1E] mb-2">
            Раздел в разработке
          </h3>
          <p className="text-sm text-[#999999] text-center max-w-xs">
            Здесь будет расширенный функционал списка дел
          </p>
        </div>
      </div>
    </motion.div>
  );
};
