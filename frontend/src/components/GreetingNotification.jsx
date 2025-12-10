import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sun, Moon, Droplets, Wind } from 'lucide-react';

// Standalone версия компонента для показа в очереди
export const GreetingNotificationContent = ({ greeting, onClose }) => {
  const hasWeather = greeting.weather != null;
  
  return (
    <motion.div
      key={greeting.type}
      initial={{ y: -20, opacity: 0, scale: 0.9 }}
      animate={{ y: 0, opacity: 1, scale: 1 }}
      exit={{ 
        opacity: 0, 
        scale: 0.9,
        transition: { duration: 0.4, ease: "easeInOut" } 
      }}
      transition={{ type: "spring", stiffness: 200, damping: 25 }}
      className="fixed top-4 left-0 right-0 mx-auto z-[90] w-[95%] md:w-auto md:max-w-md flex justify-center pointer-events-none"
    >
      <div 
        onClick={onClose}
        className={`cursor-pointer active:scale-95 transition-transform pointer-events-auto w-full max-w-sm backdrop-blur-xl px-4 py-3 rounded-2xl shadow-2xl border 
        ${greeting.type === 'morning' 
          ? 'bg-gradient-to-br from-orange-500 to-amber-500 border-orange-300/30 text-white shadow-orange-500/25' 
          : 'bg-gradient-to-br from-indigo-800 to-blue-900 border-indigo-400/30 text-white shadow-indigo-500/25'
        }`}
      >
        <div className="flex items-center gap-3">
          <div className={`p-2 rounded-full flex-shrink-0 ${greeting.type === 'morning' ? 'bg-white/25' : 'bg-white/15'}`}>
            {greeting.type === 'morning' ? (
              <Sun className="w-6 h-6 text-yellow-100" />
            ) : (
              <Moon className="w-6 h-6 text-blue-200" />
            )}
          </div>
          
          <div className="flex-1 min-w-0">
            <h3 className="font-bold text-sm truncate">
              {greeting.title}
            </h3>
            <p className="text-xs text-white/95 leading-tight mt-0.5">
              {greeting.message}
            </p>
          </div>
        </div>
        
        {/* Погода для уведомлений */}
        {hasWeather && (
          <div className="mt-3 pt-3 border-t border-white/25">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="text-2xl">{greeting.weather.icon}</span>
                <div>
                  <div className="flex items-baseline gap-1">
                    <span className="text-xl font-bold">{greeting.weather.temperature}°</span>
                    <span className="text-xs text-white/80">Москва</span>
                  </div>
                  <p className="text-xs text-white/90">{greeting.weather.description}</p>
                </div>
              </div>
              <div className="flex gap-3 text-xs text-white/80">
                <div className="flex items-center gap-1">
                  <Droplets className="w-3 h-3" />
                  <span>{greeting.weather.humidity}%</span>
                </div>
                <div className="flex items-center gap-1">
                  <Wind className="w-3 h-3" />
                  <span>{greeting.weather.wind_speed} км/ч</span>
                </div>
              </div>
            </div>
            <p className="text-xs text-white/70 mt-1">
              Ощущается как {greeting.weather.feels_like}°
            </p>
          </div>
        )}
      </div>
    </motion.div>
  );
};

export const GreetingNotification = ({ userFirstName, testHour = null, onRequestShow }) => {
  const [greeting, setGreeting] = useState(null);

  useEffect(() => {
    // Check if we already showed greeting this session (skip check if testing)
    if (!testHour && sessionStorage.getItem('greetingShown')) return;

    const checkTime = async () => {
      const now = new Date();
      const hour = testHour !== null ? testHour : now.getHours();
      
      let type = null;
      let title = "";
      let message = "";
      let weather = null;

      // Функция загрузки погоды
      const loadWeather = async () => {
        try {
          let backendUrl = '';
          try {
            if (import.meta.env.VITE_BACKEND_URL) {
              backendUrl = import.meta.env.VITE_BACKEND_URL;
            } else if (import.meta.env.REACT_APP_BACKEND_URL) {
              backendUrl = import.meta.env.REACT_APP_BACKEND_URL;
            }
          } catch (e) {
            // Ignore environment variable access errors
          }
          
          if (!backendUrl || backendUrl.trim() === '') {
            if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
              backendUrl = 'http://localhost:8001';
            } else {
              backendUrl = window.location.origin;
            }
          }
          
          const response = await fetch(`${backendUrl}/api/weather`);
          if (response.ok) {
            return await response.json();
          }
        } catch (err) {
          console.error('Error loading weather for greeting:', err);
        }
        return null;
      };

      // Morning: 04:00 - 11:59
      if (hour >= 4 && hour < 12) {
        type = 'morning';
        title = userFirstName ? `Доброе утро, ${userFirstName}!` : 'Доброе утро!';
        message = 'Желаем продуктивного дня и отличного настроения ✨';
        weather = await loadWeather();
      } 
      // Night: 22:00 - 03:59
      else if (hour >= 22 || hour < 4) {
        type = 'night';
        title = userFirstName ? `Доброй ночи, ${userFirstName}!` : 'Доброй ночи!';
        message = 'Пора отдыхать и набираться сил перед завтрашним днем 🌙';
        weather = await loadWeather();
      }

      if (type) {
        const greetingData = { type, title, message, weather };
        
        if (!testHour) {
          sessionStorage.setItem('greetingShown', 'true');
        }
        
        // Если есть callback для очереди - используем его
        if (onRequestShow) {
          onRequestShow(greetingData);
        } else {
          // Fallback на старое поведение
          setGreeting(greetingData);
          setTimeout(() => {
            setGreeting(null);
          }, 10000); // 10 секунд для показа уведомления с погодой
        }
      }
    };

    // Small delay to ensure app is loaded and transition is smooth
    // If testing, run immediately
    const delay = testHour !== null ? 100 : 1000;
    const timer = setTimeout(checkTime, delay);
    return () => clearTimeout(timer);
  }, [userFirstName, testHour, onRequestShow]);

  // Если используем очередь, не рендерим ничего здесь
  if (onRequestShow) {
    return null;
  }

  // Fallback рендеринг для обратной совместимости
  return (
    <AnimatePresence>
      {greeting && (
        <GreetingNotificationContent 
          greeting={greeting} 
          onClose={() => setGreeting(null)} 
        />
      )}
    </AnimatePresence>
  );
};
