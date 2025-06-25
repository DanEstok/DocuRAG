"""FastAPI application for DocuRAG."""

import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
import uvicorn

from .rag_chain import RAGChain
from .config import settings
from .schemas import (
    QueryRequest, 
    QueryResponse, 
    RefreshRequest, 
    RefreshResponse, 
    HealthResponse
)

# Initialize FastAPI app
app = FastAPI(
    title="DocuRAG API",
    description="Document Retrieval-Augmented Generation API",
    version="1.0.0",
    debug=settings.debug
)

# Global variables
rag_chain: Optional[RAGChain] = None
executor = ThreadPoolExecutor(max_workers=settings.max_workers)


@app.on_event("startup")
async def startup_event():
    """Initialize the RAG chain on startup."""
    global rag_chain
    
    print(f"Starting DocuRAG in {settings.environment} mode")
    print(f"Using mock LLM: {settings.should_use_mock_llm}")
    
    try:
        rag_chain = RAGChain(
            index_path=settings.index_path, 
            store_type=settings.vector_store
        )
        print(f"RAG chain initialized with {settings.vector_store} store at {settings.index_path}")
    except Exception as e:
        print(f"Warning: Could not initialize RAG chain: {e}")
        if settings.is_development:
            print("This is normal in development mode - create test data first")
        rag_chain = None


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    executor.shutdown(wait=True)


@app.get("/healthz", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    status = "healthy" if rag_chain is not None else "unhealthy"
    
    # In development mode, provide more detailed status
    if settings.is_development and rag_chain is None:
        status = "development_mode_no_index"
    
    return HealthResponse(
        status=status,
        version="1.0.0"
    )


@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query documents using RAG."""
    if rag_chain is None:
        raise HTTPException(status_code=503, detail="RAG chain not initialized")
    
    try:
        # Run query in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        answer, sources = await loop.run_in_executor(
            executor,
            rag_chain.query,
            request.question,
            request.chat_history
        )
        
        return QueryResponse(answer=answer, sources=sources)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.post("/refresh", response_model=RefreshResponse)
async def refresh_index(request: RefreshRequest, background_tasks: BackgroundTasks):
    """Refresh the vector index."""
    if rag_chain is None:
        raise HTTPException(status_code=503, detail="RAG chain not initialized")
    
    try:
        # Run refresh in thread pool
        loop = asyncio.get_event_loop()
        documents_processed = await loop.run_in_executor(
            executor,
            rag_chain.refresh_index,
            request.pdf_dir
        )
        
        return RefreshResponse(
            message="Index refreshed successfully",
            documents_processed=documents_processed
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Refresh failed: {str(e)}")


@app.post("/query/stream")
async def query_documents_stream(request: QueryRequest):
    """Stream query response token by token (stretch goal)."""
    if rag_chain is None:
        raise HTTPException(status_code=503, detail="RAG chain not initialized")
    
    async def generate_stream():
        try:
            # This is a simplified streaming implementation
            # In a real implementation, you'd need to modify the chain to support streaming
            answer, sources = await asyncio.get_event_loop().run_in_executor(
                executor,
                rag_chain.query,
                request.question,
                request.chat_history
            )
            
            # Simulate token-by-token streaming
            for token in answer.split():
                yield f"data: {token} \n\n"
                await asyncio.sleep(0.05)  # Simulate processing time
            
            # Send sources at the end
            yield f"data: [SOURCES] {len(sources)} documents\n\n"
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )


@app.post("/upload")
async def upload_documents(files: list = None):
    """Upload documents for automatic processing (stretch goal)."""
    # This is a placeholder for the upload functionality
    # In a real implementation, you would:
    # 1. Accept file uploads
    # 2. Validate file types (PDF)
    # 3. Save files to the data directory
    # 4. Trigger index refresh
    raise HTTPException(status_code=501, detail="Upload endpoint not yet implemented")


if __name__ == "__main__":
    uvicorn.run(
        "src.app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.is_development,
        log_level=settings.log_level.lower()
    )