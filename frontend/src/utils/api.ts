import axios from 'axios'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth headers here if needed
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Handle common errors
    if (error.response?.status === 503) {
      // Service unavailable - likely RAG chain not initialized
      error.message = 'Service is initializing. Please try again in a moment.'
    } else if (error.response?.status === 500) {
      error.message = 'Internal server error. Please try again.'
    } else if (error.code === 'ECONNABORTED') {
      error.message = 'Request timeout. Please try again.'
    }
    
    return Promise.reject(error)
  }
)

// API types
export interface QueryRequest {
  question: string
  chat_history?: [string, string][]
}

export interface SourceDocument {
  file_name: string
  page_number?: number
  excerpt: string
}

export interface QueryResponse {
  answer: string
  sources: SourceDocument[]
}

export interface RefreshRequest {
  pdf_dir?: string
}

export interface RefreshResponse {
  message: string
  documents_processed: number
}

export interface HealthResponse {
  status: string
  version: string
}

// API functions
export const healthCheck = async (): Promise<HealthResponse> => {
  const response = await api.get('/healthz')
  return response.data
}

export const queryDocuments = async (request: QueryRequest): Promise<QueryResponse> => {
  const response = await api.post('/query', request)
  return response.data
}

export const refreshIndex = async (request: RefreshRequest = {}): Promise<RefreshResponse> => {
  const response = await api.post('/refresh', request)
  return response.data
}

// Streaming query (for future implementation)
export const queryDocumentsStream = async (
  request: QueryRequest,
  onToken: (token: string) => void,
  onComplete: () => void,
  onError: (error: Error) => void
) => {
  try {
    const response = await fetch('/api/query/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body?.getReader()
    if (!reader) {
      throw new Error('No response body')
    }

    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      
      if (done) {
        onComplete()
        break
      }

      const chunk = decoder.decode(value)
      const lines = chunk.split('\n')

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6)
          if (data === '[DONE]') {
            onComplete()
            return
          } else if (data.startsWith('[ERROR]')) {
            onError(new Error(data.slice(8)))
            return
          } else if (data.startsWith('[SOURCES]')) {
            // Handle sources information
            continue
          } else {
            onToken(data + ' ')
          }
        }
      }
    }
  } catch (error) {
    onError(error as Error)
  }
}

export default api