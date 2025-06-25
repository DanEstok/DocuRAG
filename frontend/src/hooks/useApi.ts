import { useState, useEffect } from 'react'
import { healthCheck, HealthResponse } from '../utils/api'

// Custom hook for API health status
export const useHealthCheck = () => {
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const checkHealth = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await healthCheck()
      setHealth(response)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Health check failed')
      setHealth(null)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    checkHealth()
    
    // Check health every 30 seconds
    const interval = setInterval(checkHealth, 30000)
    
    return () => clearInterval(interval)
  }, [])

  return { health, loading, error, refetch: checkHealth }
}

// Custom hook for managing chat history
export const useChatHistory = () => {
  const [messages, setMessages] = useState<Array<{
    id: string
    type: 'user' | 'assistant'
    content: string
    sources?: Array<{
      file_name: string
      page_number?: number
      excerpt: string
    }>
    timestamp: Date
  }>>([])

  const addMessage = (
    type: 'user' | 'assistant',
    content: string,
    sources?: Array<{
      file_name: string
      page_number?: number
      excerpt: string
    }>
  ) => {
    const newMessage = {
      id: Date.now().toString(),
      type,
      content,
      sources,
      timestamp: new Date(),
    }
    setMessages(prev => [...prev, newMessage])
    return newMessage.id
  }

  const updateMessage = (id: string, content: string) => {
    setMessages(prev =>
      prev.map(msg =>
        msg.id === id ? { ...msg, content } : msg
      )
    )
  }

  const clearHistory = () => {
    setMessages([])
  }

  const getChatHistory = (): [string, string][] => {
    const history: [string, string][] = []
    for (let i = 0; i < messages.length - 1; i += 2) {
      const userMsg = messages[i]
      const assistantMsg = messages[i + 1]
      if (userMsg?.type === 'user' && assistantMsg?.type === 'assistant') {
        history.push([userMsg.content, assistantMsg.content])
      }
    }
    return history
  }

  return {
    messages,
    addMessage,
    updateMessage,
    clearHistory,
    getChatHistory,
  }
}

// Custom hook for local storage
export const useLocalStorage = <T>(key: string, initialValue: T) => {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error)
      return initialValue
    }
  })

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value
      setStoredValue(valueToStore)
      window.localStorage.setItem(key, JSON.stringify(valueToStore))
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error)
    }
  }

  return [storedValue, setValue] as const
}

// Custom hook for debounced values
export const useDebounce = <T>(value: T, delay: number): T => {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => {
      clearTimeout(handler)
    }
  }, [value, delay])

  return debouncedValue
}