"""Configuration management for DocuRAG."""

import os
from enum import Enum
from typing import Optional, Literal
from pydantic_settings import BaseSettings
from pydantic import Field


class Environment(str, Enum):
    """Environment types."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Application settings."""
    
    # Environment
    environment: Environment = Field(
        default=Environment.DEVELOPMENT,
        env="ENVIRONMENT",
        description="Application environment"
    )
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-3.5-turbo", env="OPENAI_MODEL")
    openai_embedding_model: str = Field(
        default="text-embedding-ada-002", 
        env="OPENAI_EMBEDDING_MODEL"
    )
    
    # Vector Store Configuration
    vector_store: Literal["faiss", "chroma"] = Field(
        default="faiss", 
        env="VECTOR_STORE"
    )
    index_path: str = Field(default="./index", env="INDEX_PATH")
    
    # Document Processing
    chunk_size: int = Field(default=1000, env="CHUNK_SIZE")
    chunk_overlap: int = Field(default=100, env="CHUNK_OVERLAP")
    
    # Development/Testing
    use_mock_llm: bool = Field(default=False, env="USE_MOCK_LLM")
    mock_response_delay: float = Field(default=1.0, env="MOCK_RESPONSE_DELAY")
    test_data_dir: str = Field(default="data/dev", env="TEST_DATA_DIR")
    
    # Performance
    max_workers: int = Field(default=4, env="MAX_WORKERS")
    retrieval_k: int = Field(default=4, env="RETRIEVAL_K")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == Environment.DEVELOPMENT
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing mode."""
        return self.environment == Environment.TESTING
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment == Environment.PRODUCTION
    
    @property
    def should_use_mock_llm(self) -> bool:
        """Determine if mock LLM should be used."""
        if self.use_mock_llm:
            return True
        
        # Auto-enable mock LLM in development if no API key
        if self.is_development and not self.openai_api_key:
            return True
        
        # Always use mock in testing
        if self.is_testing:
            return True
        
        return False
    
    def validate_production_config(self) -> None:
        """Validate configuration for production deployment."""
        if self.is_production:
            if not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required in production")
            
            if self.debug:
                raise ValueError("DEBUG should be False in production")
            
            if self.use_mock_llm:
                raise ValueError("USE_MOCK_LLM should be False in production")


# Global settings instance
settings = Settings()

# Validate production config on import
if settings.is_production:
    settings.validate_production_config()