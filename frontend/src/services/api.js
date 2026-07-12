import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
  timeout: 60000,
});

export const sendMessage = async (conversationId, message, stream = false) => {
  const response = await api.post('/chat', {
    conversation_id: conversationId,
    message,
    stream,
  });
  return response.data;
};

export const sendMessageStream = async (conversationId, message, onToken, onDone, onError) => {
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ conversation_id: conversationId, message, stream: true }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop();

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6));
            if (data.error) {
              onError(data.error);
              return;
            }
            if (data.done) {
              onDone(data.conversation_id);
              return;
            }
            if (data.token) {
              onToken(data.token);
            }
          } catch (e) {
            // skip malformed JSON
          }
        }
      }
    }
    onDone(conversationId);
  } catch (err) {
    onError(err.message || 'Stream failed');
  }
};

export const getConversations = async () => {
  const response = await api.get('/conversations');
  return response.data;
};

export const getConversation = async (conversationId) => {
  const response = await api.get(`/conversations/${conversationId}`);
  return response.data;
};

export const deleteConversation = async (conversationId) => {
  const response = await api.delete(`/conversations/${conversationId}`);
  return response.data;
};

export default api;
