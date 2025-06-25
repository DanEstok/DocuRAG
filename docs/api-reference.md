# DocuRAG API Reference

## Overview

The DocuRAG API provides endpoints for querying documents using retrieval-augmented generation (RAG). The API is built with FastAPI and supports both synchronous and streaming responses.

**Base URL**: `http://localhost:8000`

## Authentication

Currently, the API does not require authentication. In production deployments, consider adding API key authentication or other security measures.

## Endpoints

### Health Check

#### `GET /healthz`

Check the health status of the API service.

**Response**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

**Status Codes**
- `200`: Service is healthy
- `503`: Service is unhealthy (RAG chain not initialized)

**Example**
```bash
curl http://localhost:8000/healthz
```

### Query Documents

#### `POST /query`

Query documents using natural language questions with optional conversational context.

**Request Body**
```json
{
  "question": "string",
  "chat_history": [
    ["human message", "ai response"],
    ["human message", "ai response"]
  ]
}
```

**Parameters**
- `question` (required): The question to ask about the documents
- `chat_history` (optional): Previous conversation history as pairs of human/AI messages

**Response**
```json
{
  "answer": "string",
  "sources": [
    {
      "file_name": "document.pdf",
      "page_number": 1,
      "excerpt": "Relevant text excerpt..."
    }
  ]
}
```

**Response Fields**
- `answer`: Generated answer based on retrieved documents
- `sources`: List of source documents used to generate the answer
  - `file_name`: Name of the source PDF file
  - `page_number`: Page number in the document (may be null)
  - `excerpt`: Relevant text excerpt (truncated to 200 characters)

**Status Codes**
- `200`: Successful query
- `422`: Invalid request format
- `500`: Internal server error
- `503`: Service unavailable (RAG chain not initialized)

**Example**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the main findings of the research?",
    "chat_history": [
      ["Hello", "Hi! How can I help you with the documents?"]
    ]
  }'
```

### Refresh Index

#### `POST /refresh`

Rebuild the vector index from new or updated documents.

**Request Body**
```json
{
  "pdf_dir": "/path/to/pdf/directory"
}
```

**Parameters**
- `pdf_dir` (optional): Directory containing PDF files to index. Defaults to `./data`

**Response**
```json
{
  "message": "Index refreshed successfully",
  "documents_processed": 42
}
```

**Response Fields**
- `message`: Status message
- `documents_processed`: Number of document chunks processed

**Status Codes**
- `200`: Index refreshed successfully
- `422`: Invalid request format
- `500`: Refresh failed
- `503`: Service unavailable

**Example**
```bash
curl -X POST http://localhost:8000/refresh \
  -H "Content-Type: application/json" \
  -d '{"pdf_dir": "./new_documents"}'
```

### Streaming Query (Stretch Goal)

#### `POST /query/stream`

Query documents with streaming token-by-token response.

**Request Body**
Same as `/query` endpoint.

**Response**
Server-Sent Events (SSE) stream with `text/plain` content type.

**Stream Format**
```
data: token1 
data: token2 
data: token3 
...
data: [SOURCES] 3 documents
data: [DONE]
```

**Status Codes**
- `200`: Streaming response started
- `422`: Invalid request format
- `503`: Service unavailable

**Example**
```bash
curl -X POST http://localhost:8000/query/stream \
  -H "Content-Type: application/json" \
  -d '{"question": "Summarize the document"}' \
  --no-buffer
```

## Error Handling

### Error Response Format
```json
{
  "detail": "Error description"
}
```

### Common Errors

**Validation Error (422)**
```json
{
  "detail": [
    {
      "loc": ["body", "question"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Service Unavailable (503)**
```json
{
  "detail": "RAG chain not initialized"
}
```

**Internal Server Error (500)**
```json
{
  "detail": "Query failed: OpenAI API error"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. In production, consider implementing:
- Request rate limiting per IP/user
- Concurrent request limits
- Token usage tracking

## Request/Response Examples

### Simple Query
```bash
# Request
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is machine learning?"}'

# Response
{
  "answer": "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed...",
  "sources": [
    {
      "file_name": "ml_guide.pdf",
      "page_number": 1,
      "excerpt": "Machine learning algorithms build mathematical models based on training data..."
    }
  ]
}
```

### Conversational Query
```bash
# Request
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Can you explain that in simpler terms?",
    "chat_history": [
      ["What is machine learning?", "Machine learning is a subset of artificial intelligence..."]
    ]
  }'

# Response
{
  "answer": "In simple terms, machine learning is like teaching a computer to recognize patterns...",
  "sources": [...]
}
```

### Health Check
```bash
# Request
curl http://localhost:8000/healthz

# Response
{
  "status": "healthy",
  "version": "1.0.0"
}
```

## Client Libraries

### Python
```python
import requests

class DocuRAGClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def query(self, question, chat_history=None):
        response = requests.post(
            f"{self.base_url}/query",
            json={"question": question, "chat_history": chat_history}
        )
        return response.json()
    
    def refresh(self, pdf_dir=None):
        response = requests.post(
            f"{self.base_url}/refresh",
            json={"pdf_dir": pdf_dir}
        )
        return response.json()

# Usage
client = DocuRAGClient()
result = client.query("What are the key findings?")
print(result["answer"])
```

### JavaScript
```javascript
class DocuRAGClient {
    constructor(baseUrl = "http://localhost:8000") {
        this.baseUrl = baseUrl;
    }
    
    async query(question, chatHistory = null) {
        const response = await fetch(`${this.baseUrl}/query`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                question: question,
                chat_history: chatHistory
            })
        });
        return await response.json();
    }
    
    async refresh(pdfDir = null) {
        const response = await fetch(`${this.baseUrl}/refresh`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({pdf_dir: pdfDir})
        });
        return await response.json();
    }
}

// Usage
const client = new DocuRAGClient();
client.query("What are the main points?").then(result => {
    console.log(result.answer);
});
```

## OpenAPI Specification

The API automatically generates OpenAPI (Swagger) documentation available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## Performance Considerations

### Response Times
- Simple queries: 1-3 seconds
- Complex queries: 3-10 seconds
- Streaming responses: Real-time token delivery

### Concurrent Requests
- Default thread pool: 4 workers
- Recommended max concurrent requests: 10-20
- Consider load balancing for higher throughput

### Optimization Tips
1. Use conversational context to reduce processing time
2. Cache frequently asked questions
3. Implement request deduplication
4. Monitor and optimize chunk retrieval parameters