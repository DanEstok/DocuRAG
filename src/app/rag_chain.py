"""RAG chain implementation using LangChain."""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document
from langchain.vectorstores import FAISS, Chroma

from .schemas import SourceDocument
from .config import settings
from .mock_llm import MockEmbeddings, MockLLM, MockConversationalRetrievalChain


class RAGChain:
    """RAG chain for question answering with conversational memory."""
    
    def __init__(self, index_path: str, store_type: str = "faiss"):
        """Initialize the RAG chain.
        
        Args:
            index_path: Path to the vector index
            store_type: Type of vector store (faiss or chroma)
        """
        self.index_path = index_path
        self.store_type = store_type
        self.vectorstore = None
        self.chain = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        self._load_vectorstore()
        self._setup_chain()
    
    def _load_vectorstore(self) -> None:
        """Load the vector store from disk."""
        if not os.path.exists(self.index_path):
            raise FileNotFoundError(f"Index not found at {self.index_path}")
        
        # Choose embeddings based on configuration
        if settings.should_use_mock_llm:
            embeddings = MockEmbeddings()
            print("Using mock embeddings for development")
        else:
            embeddings = OpenAIEmbeddings(
                openai_api_key=settings.openai_api_key,
                model=settings.openai_embedding_model
            )
            print("Using OpenAI embeddings for production")
        
        if self.store_type == "faiss":
            self.vectorstore = FAISS.load_local(self.index_path, embeddings)
        elif self.store_type == "chroma":
            self.vectorstore = Chroma(
                persist_directory=self.index_path,
                embedding_function=embeddings
            )
        else:
            raise ValueError(f"Unsupported store type: {self.store_type}")
    
    def _setup_chain(self) -> None:
        """Setup the conversational retrieval chain."""
        # Choose LLM based on configuration
        if settings.should_use_mock_llm:
            llm = MockLLM(response_delay=settings.mock_response_delay)
            print("Using mock LLM for development")
            
            # Use mock chain for development
            self.chain = MockConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=self.vectorstore.as_retriever(search_kwargs={"k": settings.retrieval_k}),
                memory=self.memory,
                return_source_documents=True,
                verbose=settings.debug
            )
        else:
            llm = ChatOpenAI(
                temperature=0, 
                model_name=settings.openai_model,
                openai_api_key=settings.openai_api_key
            )
            print(f"Using OpenAI LLM: {settings.openai_model}")
            
            self.chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=self.vectorstore.as_retriever(search_kwargs={"k": settings.retrieval_k}),
                memory=self.memory,
                return_source_documents=True,
                verbose=settings.debug
            )
    
    def query(
        self, 
        question: str, 
        chat_history: Optional[List[List[str]]] = None
    ) -> Tuple[str, List[SourceDocument]]:
        """Query the RAG chain.
        
        Args:
            question: The question to ask
            chat_history: Previous chat history as list of [human, ai] pairs
            
        Returns:
            Tuple of (answer, source_documents)
        """
        # Format chat history for LangChain
        formatted_history = []
        if chat_history:
            for human, ai in chat_history:
                formatted_history.extend([
                    ("human", human),
                    ("ai", ai)
                ])
        
        # Query the chain
        result = self.chain({
            "question": question,
            "chat_history": formatted_history
        })
        
        # Extract source documents
        sources = []
        for doc in result.get("source_documents", []):
            source = SourceDocument(
                file_name=doc.metadata.get("file_name", "unknown"),
                page_number=doc.metadata.get("page", None),
                excerpt=doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            )
            sources.append(source)
        
        return result["answer"], sources
    
    def refresh_index(self, pdf_dir: Optional[str] = None) -> int:
        """Refresh the vector index.
        
        Args:
            pdf_dir: Directory containing PDF files to index
            
        Returns:
            Number of documents processed
        """
        from ..ingest.build_index import build_index
        from ..ingest.loader import PDFLoader
        
        if pdf_dir is None:
            pdf_dir = settings.test_data_dir if settings.is_development else "./data"
        
        # Build new index
        build_index(
            pdf_dir=pdf_dir,
            output_dir=self.index_path,
            store_type=self.store_type,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
        
        # Reload vectorstore
        self._load_vectorstore()
        self._setup_chain()
        
        # Count documents
        loader = PDFLoader(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
        documents = loader.load_directory(pdf_dir)
        
        return len(documents)