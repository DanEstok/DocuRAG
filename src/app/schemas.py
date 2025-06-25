"""Pydantic schemas for API requests and responses."""

from typing import List, Optional

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request schema for query endpoint."""
    
    question: str = Field(..., description="The question to ask")
    chat_history: Optional[List[List[str]]] = Field(
        default=None, 
        description="Previous chat history as list of [human, ai] pairs"
    )


class SourceDocument(BaseModel):
    """Source document information."""
    
    file_name: str = Field(..., description="Name of the source file")
    page_number: Optional[int] = Field(None, description="Page number in the document")
    excerpt: str = Field(..., description="Relevant text excerpt")


class QueryResponse(BaseModel):
    """Response schema for query endpoint."""
    
    answer: str = Field(..., description="The generated answer")
    sources: List[SourceDocument] = Field(..., description="List of source documents")


class RefreshRequest(BaseModel):
    """Request schema for refresh endpoint."""
    
    pdf_dir: Optional[str] = Field(None, description="Directory containing PDF files to index")


class RefreshResponse(BaseModel):
    """Response schema for refresh endpoint."""
    
    message: str = Field(..., description="Status message")
    documents_processed: int = Field(..., description="Number of documents processed")


class HealthResponse(BaseModel):
    """Response schema for health endpoint."""
    
    status: str = Field(..., description="Health status")
    version: str = Field(..., description="API version")