"""Tests for ingestion functionality."""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from langchain.schema import Document

from src.ingest.loader import PDFLoader
from src.ingest.build_index import build_index


class TestPDFLoader:
    """Test PDF loader functionality."""
    
    def test_init(self):
        """Test PDFLoader initialization."""
        loader = PDFLoader(chunk_size=500, chunk_overlap=50)
        assert loader.chunk_size == 500
        assert loader.chunk_overlap == 50
    
    @patch('src.ingest.loader.PyPDFLoader')
    def test_load_pdf(self, mock_pdf_loader):
        """Test loading a single PDF file."""
        # Mock PyPDFLoader
        mock_loader_instance = MagicMock()
        mock_pdf_loader.return_value = mock_loader_instance
        
        # Mock documents
        mock_doc = Document(
            page_content="This is a test document content.",
            metadata={"page": 1}
        )
        mock_loader_instance.load.return_value = [mock_doc]
        
        loader = PDFLoader(chunk_size=100, chunk_overlap=10)
        documents = loader.load_pdf("test.pdf")
        
        assert len(documents) > 0
        assert documents[0].metadata["file_name"] == "test.pdf"
        mock_pdf_loader.assert_called_once_with("test.pdf")
    
    def test_load_directory_not_exists(self):
        """Test loading from non-existent directory."""
        loader = PDFLoader()
        
        with pytest.raises(FileNotFoundError):
            loader.load_directory("/non/existent/path")
    
    def test_load_directory_no_pdfs(self):
        """Test loading from directory with no PDF files."""
        loader = PDFLoader()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(ValueError, match="No PDF files found"):
                loader.load_directory(temp_dir)


class TestBuildIndex:
    """Test index building functionality."""
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('src.ingest.build_index.PDFLoader')
    @patch('src.ingest.build_index.OpenAIEmbeddings')
    @patch('src.ingest.build_index.FAISS')
    def test_build_faiss_index(self, mock_faiss, mock_embeddings, mock_loader):
        """Test building FAISS index."""
        # Mock loader
        mock_loader_instance = MagicMock()
        mock_loader.return_value = mock_loader_instance
        mock_loader_instance.load_directory.return_value = [
            Document(page_content="test", metadata={})
        ]
        
        # Mock FAISS
        mock_vectorstore = MagicMock()
        mock_faiss.from_documents.return_value = mock_vectorstore
        
        with tempfile.TemporaryDirectory() as temp_dir:
            build_index(
                pdf_dir="./test_pdfs",
                output_dir=temp_dir,
                store_type="faiss"
            )
            
            mock_faiss.from_documents.assert_called_once()
            mock_vectorstore.save_local.assert_called_once_with(temp_dir)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('src.ingest.build_index.PDFLoader')
    @patch('src.ingest.build_index.OpenAIEmbeddings')
    @patch('src.ingest.build_index.Chroma')
    def test_build_chroma_index(self, mock_chroma, mock_embeddings, mock_loader):
        """Test building Chroma index."""
        # Mock loader
        mock_loader_instance = MagicMock()
        mock_loader.return_value = mock_loader_instance
        mock_loader_instance.load_directory.return_value = [
            Document(page_content="test", metadata={})
        ]
        
        # Mock Chroma
        mock_vectorstore = MagicMock()
        mock_chroma.from_documents.return_value = mock_vectorstore
        
        with tempfile.TemporaryDirectory() as temp_dir:
            build_index(
                pdf_dir="./test_pdfs",
                output_dir=temp_dir,
                store_type="chroma"
            )
            
            mock_chroma.from_documents.assert_called_once()
            mock_vectorstore.persist.assert_called_once()
    
    def test_build_index_no_api_key(self):
        """Test building index without OpenAI API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="OPENAI_API_KEY"):
                build_index("./test_pdfs", "./test_index")
    
    def test_build_index_invalid_store_type(self):
        """Test building index with invalid store type."""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            with pytest.raises(ValueError, match="Unsupported store type"):
                build_index("./test_pdfs", "./test_index", store_type="invalid")