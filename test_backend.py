"""Simplified backend for testing frontend integration."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import time
import uvicorn

# Schemas
class QueryRequest(BaseModel):
    question: str = Field(..., description="The question to ask")
    chat_history: Optional[List[List[str]]] = Field(
        default=None, 
        description="Previous chat history as list of [human, ai] pairs"
    )

class SourceDocument(BaseModel):
    file_name: str = Field(..., description="Name of the source file")
    page_number: Optional[int] = Field(None, description="Page number in the document")
    excerpt: str = Field(..., description="Relevant text excerpt")

class QueryResponse(BaseModel):
    answer: str = Field(..., description="The generated answer")
    sources: List[SourceDocument] = Field(..., description="List of source documents")

class RefreshRequest(BaseModel):
    pdf_dir: Optional[str] = Field(None, description="Directory containing PDF files to index")

class RefreshResponse(BaseModel):
    message: str = Field(..., description="Status message")
    documents_processed: int = Field(..., description="Number of documents processed")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status")
    version: str = Field(..., description="API version")

# FastAPI app
app = FastAPI(
    title="DocuRAG Test API",
    description="Test backend for DocuRAG frontend integration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data
MOCK_SOURCES = [
    SourceDocument(
        file_name="machine_learning_guide.pdf",
        page_number=15,
        excerpt="Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed."
    ),
    SourceDocument(
        file_name="ai_ethics_research.pdf", 
        page_number=23,
        excerpt="Ethical considerations in AI development include fairness, transparency, accountability, and the potential impact on society and employment."
    ),
    SourceDocument(
        file_name="data_science_handbook.pdf",
        page_number=8,
        excerpt="Data preprocessing is a crucial step in machine learning that involves cleaning, transforming, and organizing raw data for analysis."
    )
]

MOCK_RESPONSES = {
    "machine learning": "Machine learning is a powerful subset of artificial intelligence that enables computers to learn patterns from data without being explicitly programmed. It involves algorithms that can automatically improve their performance through experience. The main types include supervised learning (with labeled data), unsupervised learning (finding patterns in unlabeled data), and reinforcement learning (learning through interaction with an environment).",
    
    "ai ethics": "AI ethics encompasses the moral principles and guidelines that govern the development and deployment of artificial intelligence systems. Key considerations include ensuring fairness and avoiding bias, maintaining transparency in decision-making processes, establishing accountability for AI actions, protecting privacy and data rights, and considering the broader societal impacts including potential job displacement and economic effects.",
    
    "data science": "Data science is an interdisciplinary field that combines statistical analysis, machine learning, and domain expertise to extract insights from data. It involves the entire data lifecycle: collection, cleaning, exploration, modeling, and interpretation. Data scientists use programming languages like Python and R, along with various tools and frameworks, to solve complex business problems and make data-driven decisions.",
    
    "default": "I'm a test AI assistant for DocuRAG. I can help you understand concepts related to machine learning, artificial intelligence, data science, and more. The documents in my knowledge base cover topics like ML algorithms, AI ethics, data preprocessing, and best practices in data science. Feel free to ask me specific questions about these topics!"
}

@app.get("/healthz", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="development_mode_no_index",
        version="1.0.0"
    )

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query documents using mock responses."""
    # Simulate processing time
    time.sleep(0.5)
    
    question_lower = request.question.lower()
    
    # Simple keyword matching for demo
    if "machine learning" in question_lower or "ml" in question_lower:
        answer = MOCK_RESPONSES["machine learning"]
        sources = [MOCK_SOURCES[0], MOCK_SOURCES[2]]
    elif "ethics" in question_lower or "ethical" in question_lower:
        answer = MOCK_RESPONSES["ai ethics"] 
        sources = [MOCK_SOURCES[1]]
    elif "data science" in question_lower or "data" in question_lower:
        answer = MOCK_RESPONSES["data science"]
        sources = [MOCK_SOURCES[2], MOCK_SOURCES[0]]
    else:
        answer = MOCK_RESPONSES["default"]
        sources = MOCK_SOURCES[:2]
    
    # Add context from chat history if available
    if request.chat_history:
        answer = f"Based on our previous conversation and the documents, {answer.lower()}"
    
    return QueryResponse(answer=answer, sources=sources)

@app.post("/refresh", response_model=RefreshResponse)
async def refresh_index(request: RefreshRequest):
    """Mock refresh endpoint."""
    # Simulate processing time
    time.sleep(1.0)
    
    return RefreshResponse(
        message="Index refreshed successfully (mock)",
        documents_processed=3
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)