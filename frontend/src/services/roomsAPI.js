/**
 * API Service для работы с комнатами (Rooms)
 */

import axios from 'axios';

// Определяем URL backend
const getBackendURL = () => {
  let envBackendUrl = '';
  
  try {
    if (typeof process !== 'undefined' && process.env && process.env.REACT_APP_BACKEND_URL) {
      envBackendUrl = process.env.REACT_APP_BACKEND_URL;
    } else if (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.REACT_APP_BACKEND_URL) {
      envBackendUrl = import.meta.env.REACT_APP_BACKEND_URL;
    }
  } catch (error) {
    console.warn('Could not access environment variables:', error);
  }
  
  if (envBackendUrl && envBackendUrl.trim() !== '') {
    return envBackendUrl;
  }
  
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://localhost:8001';
  }
  
  return window.location.origin;
};

const API_BASE_URL = getBackendURL();

console.log('🏠 Rooms API initialized with backend URL:', API_BASE_URL);

// Создать комнату
export const createRoom = async (roomData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/rooms`, roomData);
    return response.data;
  } catch (error) {
    console.error('Error creating room:', error);
    throw error;
  }
};

// Получить все комнаты пользователя
export const getUserRooms = async (telegramId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/rooms/${telegramId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching user rooms:', error);
    throw error;
  }
};

// Получить детали комнаты
export const getRoomDetail = async (roomId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/rooms/detail/${roomId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching room detail:', error);
    throw error;
  }
};

// Сгенерировать ссылку-приглашение
export const generateInviteLink = async (roomId, telegramId) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/api/rooms/${roomId}/invite-link`,
      { telegram_id: telegramId }
    );
    return response.data;
  } catch (error) {
    console.error('Error generating invite link:', error);
    throw error;
  }
};

// Присоединиться к комнате по токену
export const joinRoomByToken = async (inviteToken, joinData) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/api/rooms/join/${inviteToken}`,
      joinData
    );
    return response.data;
  } catch (error) {
    console.error('Error joining room:', error);
    throw error;
  }
};

// Создать задачу в комнате
export const createRoomTask = async (roomId, taskData) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/api/rooms/${roomId}/tasks`,
      taskData
    );
    return response.data;
  } catch (error) {
    console.error('Error creating room task:', error);
    throw error;
  }
};

// Получить все задачи комнаты
export const getRoomTasks = async (roomId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/rooms/${roomId}/tasks`);
    return response.data;
  } catch (error) {
    console.error('Error fetching room tasks:', error);
    throw error;
  }
};

// Покинуть комнату
export const leaveRoom = async (roomId, telegramId) => {
  try {
    const response = await axios.delete(
      `${API_BASE_URL}/api/rooms/${roomId}/leave`,
      { data: { telegram_id: telegramId } }
    );
    return response.data;
  } catch (error) {
    console.error('Error leaving room:', error);
    throw error;
  }
};

// Удалить комнату
export const deleteRoom = async (roomId, telegramId) => {
  try {
    const response = await axios.delete(
      `${API_BASE_URL}/api/rooms/${roomId}`,
      { data: { telegram_id: telegramId } }
    );
    return response.data;
  } catch (error) {
    console.error('Error deleting room:', error);
    throw error;
  }
};
