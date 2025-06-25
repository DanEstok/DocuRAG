"""Mock LLM and embeddings for development and testing."""

import random
import time
from typing import List, Optional, Dict, Any
import numpy as np
from langchain.schema import Document
from langchain.embeddings.base import Embeddings
from langchain.llms.base import LLM


class MockEmbeddings(Embeddings):
    """Mock embeddings that generate random vectors for development."""
    
    def __init__(self, dimension: int = 1536):
        """Initialize mock embeddings.
        
        Args:
            dimension: Dimension of embedding vectors (matches OpenAI default)
        """
        self.dimension = dimension
        # Set seed for reproducible embeddings in tests
        self._rng = np.random.RandomState(42)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate mock embeddings for documents.
        
        Args:
            texts: List of text documents
            
        Returns:
            List of embedding vectors
        """
        embeddings = []
        for text in texts:
            # Generate deterministic embeddings based on text hash
            seed = hash(text) % (2**32)
            rng = np.random.RandomState(seed)
            embedding = rng.normal(0, 1, self.dimension).tolist()
            embeddings.append(embedding)
        
        # Simulate API delay
        time.sleep(0.1 * len(texts))
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """Generate mock embedding for a query.
        
        Args:
            text: Query text
            
        Returns:
            Embedding vector
        """
        return self.embed_documents([text])[0]


class MockLLM(LLM):
    """Mock LLM that generates realistic responses for development."""
    
    def __init__(self, response_delay: float = 1.0):
        """Initialize mock LLM.
        
        Args:
            response_delay: Simulated response delay in seconds
        """
        super().__init__()
        self.response_delay = response_delay
        self._response_templates = [
            "Based on the provided documents, {topic}. The key points include: {points}. {conclusion}",
            "According to the source material, {topic}. This is evidenced by {points}. {conclusion}",
            "The documents indicate that {topic}. Specifically, {points}. {conclusion}",
            "From the available information, {topic}. The main findings are: {points}. {conclusion}"
        ]
        
        self._topics = [
            "machine learning is a powerful technology",
            "artificial intelligence has significant implications",
            "data science involves multiple disciplines",
            "ethical considerations are important",
            "technological advancement continues rapidly"
        ]
        
        self._points = [
            "supervised and unsupervised learning approaches",
            "the importance of data quality and preprocessing",
            "various algorithms and their applications",
            "the need for responsible development practices",
            "emerging trends and future directions"
        ]
        
        self._conclusions = [
            "This represents an important area for continued research and development.",
            "These findings have significant implications for future applications.",
            "Further investigation is needed to fully understand the implications.",
            "This technology shows great promise for solving complex problems.",
            "Careful consideration of these factors is essential for success."
        ]
    
    @property
    def _llm_type(self) -> str:
        """Return LLM type."""
        return "mock"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> str:
        """Generate a mock response.
        
        Args:
            prompt: Input prompt
            stop: Stop sequences
            run_manager: Run manager
            **kwargs: Additional arguments
            
        Returns:
            Generated response
        """
        # Simulate processing time
        time.sleep(self.response_delay)
        
        # Generate response based on prompt content
        if "question" in prompt.lower() or "what" in prompt.lower():
            template = random.choice(self._response_templates)
            topic = random.choice(self._topics)
            points = random.choice(self._points)
            conclusion = random.choice(self._conclusions)
            
            response = template.format(
                topic=topic,
                points=points,
                conclusion=conclusion
            )
        else:
            # Generic response for other prompts
            response = (
                "This is a mock response generated for development purposes. "
                "In production, this would be replaced with actual LLM output. "
                "The response is based on the provided context and question."
            )
        
        return response
    
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return identifying parameters."""
        return {"response_delay": self.response_delay}


class MockConversationalRetrievalChain:
    """Mock conversational retrieval chain for development."""
    
    def __init__(self, llm, retriever, memory=None, **kwargs):
        """Initialize mock chain.
        
        Args:
            llm: Language model
            retriever: Document retriever
            memory: Conversation memory
            **kwargs: Additional arguments
        """
        self.llm = llm
        self.retriever = retriever
        self.memory = memory
        self.return_source_documents = kwargs.get("return_source_documents", True)
    
    def __call__(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Process inputs and return mock response.
        
        Args:
            inputs: Input dictionary with question and chat_history
            
        Returns:
            Response dictionary with answer and source_documents
        """
        question = inputs.get("question", "")
        chat_history = inputs.get("chat_history", [])
        
        # Simulate retrieval
        try:
            docs = self.retriever.get_relevant_documents(question)
        except Exception:
            # Fallback if retriever fails
            docs = [
                Document(
                    page_content="Mock document content for development purposes.",
                    metadata={"file_name": "mock_doc.pdf", "page": 1}
                )
            ]
        
        # Generate mock answer
        answer = self.llm._call(f"Question: {question}\nContext: {[doc.page_content[:100] for doc in docs]}")
        
        result = {"answer": answer}
        
        if self.return_source_documents:
            result["source_documents"] = docs
        
        return result
    
    @classmethod
    def from_llm(cls, llm, retriever, memory=None, **kwargs):
        """Create chain from LLM and retriever.
        
        Args:
            llm: Language model
            retriever: Document retriever
            memory: Conversation memory
            **kwargs: Additional arguments
            
        Returns:
            Mock chain instance
        """
        return cls(llm, retriever, memory, **kwargs)