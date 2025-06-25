import React, { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  PaperAirplaneIcon,
  TrashIcon,
  DocumentTextIcon,
  UserIcon,
  SparklesIcon,
  ExclamationTriangleIcon,
} from '@heroicons/react/24/outline'
import { toast } from 'react-hot-toast'
import { queryDocuments, QueryRequest } from '../utils/api'
import { useChatHistory, useHealthCheck } from '../hooks/useApi'
import LoadingSpinner from '../components/LoadingSpinner'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

const ChatPage: React.FC = () => {
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)
  
  const { messages, addMessage, clearHistory, getChatHistory } = useChatHistory()
  const { health } = useHealthCheck()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!input.trim() || isLoading) return

    const question = input.trim()
    setInput('')
    setIsLoading(true)

    // Add user message
    addMessage('user', question)

    try {
      const chatHistory = getChatHistory()
      const request: QueryRequest = {
        question,
        chat_history: chatHistory.length > 0 ? chatHistory : undefined,
      }

      const response = await queryDocuments(request)
      
      // Add assistant message with sources
      addMessage('assistant', response.answer, response.sources)
      
    } catch (error) {
      console.error('Query failed:', error)
      const errorMessage = error instanceof Error ? error.message : 'Failed to get response'
      addMessage('assistant', `Sorry, I encountered an error: ${errorMessage}`)
      toast.error('Failed to get response')
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e as React.FormEvent)
    }
  }

  const isSystemReady = health?.status === 'healthy' || health?.status === 'development_mode_no_index'

  const exampleQuestions = [
    "What are the main topics covered in the documents?",
    "Can you summarize the key findings?",
    "What is machine learning according to the documents?",
    "Tell me about artificial intelligence ethics",
  ]

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">AI Chat Assistant</h1>
          <p className="text-gray-600">Ask questions about your documents</p>
        </div>
        {messages.length > 0 && (
          <button
            onClick={clearHistory}
            className="btn-ghost text-red-600 hover:bg-red-50"
          >
            <TrashIcon className="w-4 h-4 mr-2" />
            Clear Chat
          </button>
        )}
      </div>

      {/* System Status Warning */}
      {!isSystemReady && (
        <div className="mb-4 p-4 bg-warning-50 border border-warning-200 rounded-lg">
          <div className="flex items-center space-x-2 text-warning-700">
            <ExclamationTriangleIcon className="w-5 h-5" />
            <span className="font-medium">System Not Ready</span>
          </div>
          <p className="text-warning-600 mt-1 text-sm">
            The AI system is not fully initialized. Please check the system status or try again later.
          </p>
        </div>
      )}

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto space-y-4 mb-4">
        <AnimatePresence>
          {messages.length === 0 ? (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center py-12 space-y-6"
            >
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto">
                <SparklesIcon className="w-8 h-8 text-primary-600" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  Start a conversation
                </h3>
                <p className="text-gray-600 mb-6">
                  Ask me anything about your documents. I'll provide answers with source citations.
                </p>
                
                {isSystemReady && (
                  <div className="space-y-3">
                    <p className="text-sm font-medium text-gray-700">Try these examples:</p>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-w-2xl mx-auto">
                      {exampleQuestions.map((question, index) => (
                        <button
                          key={index}
                          onClick={() => setInput(question)}
                          className="text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg text-sm text-gray-700 transition-colors"
                        >
                          "{question}"
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </motion.div>
          ) : (
            messages.map((message, index) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`flex space-x-3 max-w-3xl ${message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                    message.type === 'user' 
                      ? 'bg-primary-600 text-white' 
                      : 'bg-gray-200 text-gray-600'
                  }`}>
                    {message.type === 'user' ? (
                      <UserIcon className="w-4 h-4" />
                    ) : (
                      <SparklesIcon className="w-4 h-4" />
                    )}
                  </div>
                  
                  <div className={`rounded-lg px-4 py-3 ${
                    message.type === 'user'
                      ? 'bg-primary-600 text-white'
                      : 'bg-white border border-gray-200 shadow-sm'
                  }`}>
                    <div className={`prose prose-sm max-w-none ${
                      message.type === 'user' ? 'prose-invert' : ''
                    }`}>
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {message.content}
                      </ReactMarkdown>
                    </div>
                    
                    {message.sources && message.sources.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-gray-200">
                        <p className="text-xs font-medium text-gray-500 mb-2">Sources:</p>
                        <div className="space-y-2">
                          {message.sources.map((source, idx) => (
                            <div key={idx} className="flex items-start space-x-2 text-xs">
                              <DocumentTextIcon className="w-3 h-3 text-gray-400 mt-0.5 flex-shrink-0" />
                              <div>
                                <span className="font-medium text-gray-700">
                                  {source.file_name}
                                  {source.page_number && ` (Page ${source.page_number})`}
                                </span>
                                <p className="text-gray-600 mt-1">{source.excerpt}</p>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    <div className="text-xs text-gray-400 mt-2">
                      {message.timestamp.toLocaleTimeString()}
                    </div>
                  </div>
                </div>
              </motion.div>
            ))
          )}
        </AnimatePresence>
        
        {isLoading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex justify-start"
          >
            <div className="flex space-x-3 max-w-3xl">
              <div className="w-8 h-8 rounded-full bg-gray-200 text-gray-600 flex items-center justify-center flex-shrink-0">
                <SparklesIcon className="w-4 h-4" />
              </div>
              <div className="bg-white border border-gray-200 shadow-sm rounded-lg px-4 py-3">
                <LoadingSpinner size="sm" text="Thinking..." />
              </div>
            </div>
          </motion.div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="flex space-x-3">
        <div className="flex-1 relative">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={isSystemReady ? "Ask a question about your documents..." : "System not ready..."}
            disabled={!isSystemReady || isLoading}
            rows={1}
            className="input resize-none pr-12 min-h-[44px] max-h-32"
            style={{ height: 'auto' }}
            onInput={(e) => {
              const target = e.target as HTMLTextAreaElement
              target.style.height = 'auto'
              target.style.height = Math.min(target.scrollHeight, 128) + 'px'
            }}
          />
        </div>
        <button
          type="submit"
          disabled={!input.trim() || !isSystemReady || isLoading}
          className="btn-primary px-4 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? (
            <LoadingSpinner size="sm" />
          ) : (
            <PaperAirplaneIcon className="w-4 h-4" />
          )}
        </button>
      </form>
    </div>
  )
}

export default ChatPage