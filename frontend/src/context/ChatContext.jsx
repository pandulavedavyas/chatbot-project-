import { createContext, useContext, useState, useCallback } from 'react';
import { sendMessage as apiSendMessage, getConversations, getConversation, createConversation as apiCreateConversation, deleteConversation as apiDeleteConversation } from '../services/api';

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
      setError(err.message);
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
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const startNewConversation = useCallback(async () => {
    try {
      setCurrentConversation(null);
      setMessages([]);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  }, []);

  const sendMessage = useCallback(async (message) => {
    try {
      setIsLoading(true);
      setError(null);
      
      const userMessage = { role: 'user', content: message, timestamp: new Date().toISOString() };
      setMessages(prev => [...prev, userMessage]);
      
      const response = await apiSendMessage(currentConversation?.id, message);
      
      if (!currentConversation) {
        const newConversation = { id: response.conversation_id, title: 'New Chat' };
        setCurrentConversation(newConversation);
        await loadConversations();
      }
      
      const assistantMessage = { role: 'assistant', content: response.reply, timestamp: new Date().toISOString() };
      setMessages(prev => [...prev, assistantMessage]);
      
      return response;
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.message || 'Something went wrong';
      setError(errorMsg);
      setMessages(prev => prev.slice(0, -1));
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [currentConversation, loadConversations]);

  const deleteConversation = useCallback(async (conversationId) => {
    try {
      await apiDeleteConversation(conversationId);
      
      if (currentConversation?.id === conversationId) {
        setCurrentConversation(null);
        setMessages([]);
      }
      
      await loadConversations();
    } catch (err) {
      setError(err.message);
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
