import { createContext, useContext, useState, useCallback } from 'react';
import { sendMessage as apiSendMessage, sendMessageStream, getConversations, getConversation, deleteConversation as apiDeleteConversation } from '../services/api';

const ChatContext = createContext();

export const useChatContext = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChatContext must be used within a ChatProvider');
  }
  return context;
};

export const ChatProvider = ({ children }) => {
  const [conversations, setConversations] = useState([]);
  const [currentConversation, setCurrentConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadConversations = useCallback(async () => {
    try {
      const data = await getConversations();
      setConversations(data);
    } catch (err) {
      setError('Failed to load conversations');
    }
  }, []);

  const loadConversation = useCallback(async (conversationId) => {
    try {
      setIsLoading(true);
      const conversation = await getConversation(conversationId);
      setCurrentConversation(conversation);
      setMessages(conversation.messages || []);
      setError(null);
    } catch (err) {
      setError('Failed to load conversation');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const startNewConversation = useCallback(() => {
    setCurrentConversation(null);
    setMessages([]);
    setError(null);
  }, []);

  const sendMessage = useCallback(async (message) => {
    try {
      setIsLoading(true);
      setError(null);

      const userMessage = { role: 'user', content: message, timestamp: new Date().toISOString() };
      setMessages(prev => [...prev, userMessage]);

      const response = await apiSendMessage(currentConversation?.id, message);

      if (!currentConversation) {
        setCurrentConversation({ id: response.conversation_id, title: 'New Chat' });
        await loadConversations();
      }

      const assistantMessage = { role: 'assistant', content: response.reply, timestamp: new Date().toISOString() };
      setMessages(prev => [...prev, assistantMessage]);

      return response;
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Something went wrong. Please try again.';
      setError(errorMsg);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [currentConversation, loadConversations]);

  const sendMessageWithStream = useCallback(async (message) => {
    try {
      setIsLoading(true);
      setError(null);

      const userMessage = { role: 'user', content: message, timestamp: new Date().toISOString() };
      setMessages(prev => [...prev, userMessage]);

      let assistantContent = '';
      const assistantIndex = messages.length + 1;

      setMessages(prev => [...prev, { role: 'assistant', content: '', timestamp: new Date().toISOString(), streaming: true }]);

      await sendMessageStream(
        currentConversation?.id,
        message,
        (token) => {
          assistantContent += token;
          setMessages(prev => {
            const updated = [...prev];
            updated[assistantIndex] = { ...updated[assistantIndex], content: assistantContent };
            return updated;
          });
        },
        async (conversationId) => {
          setMessages(prev => {
            const updated = [...prev];
            updated[assistantIndex] = { ...updated[assistantIndex], streaming: false };
            return updated;
          });
          if (!currentConversation) {
            setCurrentConversation({ id: conversationId, title: 'New Chat' });
            await loadConversations();
          }
          setIsLoading(false);
        },
        (errorMsg) => {
          setError(errorMsg);
          setMessages(prev => prev.slice(0, -1));
          setIsLoading(false);
        }
      );
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Something went wrong. Please try again.';
      setError(errorMsg);
    }
  }, [currentConversation, messages.length, loadConversations]);

  const deleteConversation = useCallback(async (conversationId) => {
    try {
      await apiDeleteConversation(conversationId);
      if (currentConversation?.id === conversationId) {
        setCurrentConversation(null);
        setMessages([]);
      }
      await loadConversations();
    } catch (err) {
      setError('Failed to delete conversation');
    }
  }, [currentConversation, loadConversations]);

  const value = {
    conversations,
    currentConversation,
    messages,
    isLoading,
    error,
    loadConversations,
    loadConversation,
    startNewConversation,
    sendMessage,
    sendMessageWithStream,
    deleteConversation,
    setError,
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};

export default ChatContext;
