import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, UserCheck, Shield } from 'lucide-react';
import { updateJournalViewers } from '../../services/journalAPI';

export const JournalAccessModal = ({
  isOpen,
  onClose,
  journalId,
  students,
  currentViewerIds = [], // Array of ints
  telegramId, // Owner ID
  onUpdate // Callback to refresh journal data
}) => {
  if (!isOpen) return null;

  const linkedStudents = students.filter(s => s.is_linked && s.telegram_id);
  
  const handleToggleAccess = async (student) => {
    const hasAccess = currentViewerIds.includes(student.telegram_id);
    const action = hasAccess ? 'remove' : 'add';
    
    try {
      await updateJournalViewers(journalId, {
        telegram_id: telegramId,
        target_user_id: student.telegram_id,
        action
      });
      if (onUpdate) onUpdate();
    } catch (error) {
      console.error('Error updating access:', error);
    }
  };

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/80 backdrop-blur-sm z-[60] flex items-center justify-center p-4"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          className="bg-[#1C1C1E] rounded-2xl w-full max-w-md overflow-hidden"
          onClick={e => e.stopPropagation()}
        >
          <div className="p-4 border-b border-white/10 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Shield className="w-5 h-5 text-purple-400" />
              <h3 className="text-lg font-semibold text-white">Доступ к статистике</h3>
            </div>
            <button onClick={onClose} className="p-2 hover:bg-white/10 rounded-full text-gray-400">
              <X className="w-5 h-5" />
            </button>
          </div>
          
          <div className="p-4">
            <p className="text-sm text-gray-400 mb-4">
              Выберите студентов, которые смогут просматривать общую статистику журнала (помимо старосты).
            </p>
            
            <div className="space-y-2 max-h-[60vh] overflow-y-auto">
              {linkedStudents.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  Нет привязанных студентов.
                  <br />
                  Сначала студенты должны привязать свои аккаунты.
                </div>
              ) : (
                linkedStudents.map(student => {
                  const hasAccess = currentViewerIds.includes(student.telegram_id);
                  return (
                    <div 
                      key={student.id}
                      className="flex items-center justify-between bg-white/5 p-3 rounded-xl hover:bg-white/10 transition-colors cursor-pointer"
                      onClick={() => handleToggleAccess(student)}
                    >
                      <div className="flex items-center gap-3">
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                          hasAccess ? 'bg-purple-500/20 text-purple-400' : 'bg-gray-700 text-gray-400'
                        }`}>
                          <UserCheck className="w-4 h-4" />
                        </div>
                        <div>
                          <p className="text-white font-medium">{student.full_name}</p>
                          <p className="text-xs text-gray-400">@{student.username || 'unknown'}</p>
                        </div>
                      </div>
                      
                      <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${
                        hasAccess 
                          ? 'bg-purple-500 border-purple-500' 
                          : 'border-gray-600'
                      }`}>
                        {hasAccess && <Check className="w-3 h-3 text-white" />}
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

// Helper Check icon
const Check = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <polyline points="20 6 9 17 4 12" />
  </svg>
);
