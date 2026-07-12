import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const sendMessage = async (conversationId, message) => {
  const response = await api.post('/chat', {
    conversation_id: conversationId,
    message: message,
  });
  return response.data;
};

export const getConversations = async () => {
  const response = await api.get('/conversations');
  return response.data;
};

export const getConversation = async (conversationId) => {
  const response = await api.get(`/conversations/${conversationId}`);
  return response.data;
};

export const createConversation = async () => {
  const response = await api.post('/conversations');
  return response.data;
};

export const deleteConversation = async (conversationId) => {
  const response = await api.delete(`/conversations/${conversationId}`);
  return response.data;
};

export default api;
