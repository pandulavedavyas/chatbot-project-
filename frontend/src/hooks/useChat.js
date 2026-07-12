import { useState, useRef, useCallback, useEffect } from 'react';
import { useChatContext } from '../context/ChatContext';

export const useChat = () => {
  const { messages, isLoading, error, sendMessage, sendMessageWithStream, setError } = useChatContext();
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);
  const scrollContainerRef = useRef(null);
  const isUserAtBottom = useRef(true);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  const checkIfAtBottom = useCallback(() => {
    const container = scrollContainerRef.current;
    if (!container) return true;
    const threshold = 100;
    return container.scrollHeight - container.scrollTop - container.clientHeight < threshold;
  }, []);

  useEffect(() => {
    const container = scrollContainerRef.current;
    if (!container) return;
    const handleScroll = () => {
      isUserAtBottom.current = checkIfAtBottom();
    };
    container.addEventListener('scroll', handleScroll, { passive: true });
    return () => container.removeEventListener('scroll', handleScroll);
  }, [checkIfAtBottom]);

  useEffect(() => {
    if (isUserAtBottom.current) {
      scrollToBottom();
    }
  }, [messages, scrollToBottom]);

  const handleSend = useCallback(async () => {
    const trimmedMessage = inputValue.trim();
    if (!trimmedMessage || isLoading) return;

    setInputValue('');
    isUserAtBottom.current = true;

    try {
      await sendMessageWithStream(trimmedMessage);
    } catch (err) {
      console.error('Failed to send message:', err);
    }
  }, [inputValue, isLoading, sendMessageWithStream]);

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
    } catch {
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
    scrollContainerRef,
    handleSend,
    handleKeyDown,
    copyToClipboard,
    clearError,
  };
};

export default useChat;
