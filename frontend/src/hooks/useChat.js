import { useState, useRef, useCallback, useEffect } from 'react';
import { useChatContext } from '../context/ChatContext';

export const useChat = () => {
  const { messages, isLoading, error, sendMessage, setError } = useChatContext();
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  const handleSend = useCallback(async () => {
    const trimmedMessage = inputValue.trim();
    if (!trimmedMessage || isLoading) return;

    setInputValue('');
    
    try {
      await sendMessage(trimmedMessage);
    } catch (err) {
      console.error('Failed to send message:', err);
    }
  }, [inputValue, isLoading, sendMessage]);

  const handleKeyDown = useCallback((e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }, [handleSend]);

  const copyToClipboard = useCallback(async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (err) {
      console.error('Failed to copy:', err);
      return false;
    }
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, [setError]);

  return {
    messages,
    isLoading,
    error,
    inputValue,
    setInputValue,
    messagesEndRef,
    textareaRef,
    handleSend,
    handleKeyDown,
    copyToClipboard,
    clearError,
  };
};

export default useChat;
