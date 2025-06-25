"""Tests for FastAPI application."""

import os
from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient

from src.app.main import app
from src.app.schemas import QueryRequest, RefreshRequest


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


@pytest.fixture
def mock_rag_chain():
    """Mock RAG chain fixture."""
    mock_chain = MagicMock()
    mock_chain.query.return_value = (
        "This is a test answer.",
        [
            {
                "file_name": "test.pdf",
                "page_number": 1,
                "excerpt": "This is a test excerpt..."
            }
        ]
    )
    mock_chain.refresh_index.return_value = 5
    return mock_chain


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check_healthy(self, client):
        """Test health check when service is healthy."""
        with patch('src.app.main.rag_chain', MagicMock()):
            response = client.get("/healthz")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["version"] == "1.0.0"
    
    def test_health_check_unhealthy(self, client):
        """Test health check when service is unhealthy."""
        with patch('src.app.main.rag_chain', None):
            response = client.get("/healthz")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "unhealthy"


class TestQueryEndpoint:
    """Test query endpoint."""
    
    def test_query_success(self, client, mock_rag_chain):
        """Test successful query."""
        with patch('src.app.main.rag_chain', mock_rag_chain):
            request_data = {
                "question": "What is this document about?",
                "chat_history": [["Hello", "Hi there!"]]
            }
            
            response = client.post("/query", json=request_data)
            assert response.status_code == 200
            
            data = response.json()
            assert "answer" in data
            assert "sources" in data
            assert len(data["sources"]) > 0
    
    def test_query_no_rag_chain(self, client):
        """Test query when RAG chain is not initialized."""
        with patch('src.app.main.rag_chain', None):
            request_data = {"question": "Test question"}
            
            response = client.post("/query", json=request_data)
            assert response.status_code == 503
    
    def test_query_invalid_request(self, client):
        """Test query with invalid request data."""
        response = client.post("/query", json={})
        assert response.status_code == 422  # Validation error
    
    def test_query_chain_error(self, client):
        """Test query when chain raises an error."""
        mock_chain = MagicMock()
        mock_chain.query.side_effect = Exception("Test error")
        
        with patch('src.app.main.rag_chain', mock_chain):
            request_data = {"question": "Test question"}
            
            response = client.post("/query", json=request_data)
            assert response.status_code == 500


class TestRefreshEndpoint:
    """Test refresh endpoint."""
    
    def test_refresh_success(self, client, mock_rag_chain):
        """Test successful refresh."""
        with patch('src.app.main.rag_chain', mock_rag_chain):
            request_data = {"pdf_dir": "./test_data"}
            
            response = client.post("/refresh", json=request_data)
            assert response.status_code == 200
            
            data = response.json()
            assert data["message"] == "Index refreshed successfully"
            assert data["documents_processed"] == 5
    
    def test_refresh_no_rag_chain(self, client):
        """Test refresh when RAG chain is not initialized."""
        with patch('src.app.main.rag_chain', None):
            request_data = {"pdf_dir": "./test_data"}
            
            response = client.post("/refresh", json=request_data)
            assert response.status_code == 503
    
    def test_refresh_chain_error(self, client):
        """Test refresh when chain raises an error."""
        mock_chain = MagicMock()
        mock_chain.refresh_index.side_effect = Exception("Test error")
        
        with patch('src.app.main.rag_chain', mock_chain):
            request_data = {"pdf_dir": "./test_data"}
            
            response = client.post("/refresh", json=request_data)
            assert response.status_code == 500


class TestStreamEndpoint:
    """Test streaming endpoint."""
    
    def test_stream_success(self, client, mock_rag_chain):
        """Test successful streaming query."""
        with patch('src.app.main.rag_chain', mock_rag_chain):
            request_data = {"question": "Test streaming question"}
            
            response = client.post("/query/stream", json=request_data)
            assert response.status_code == 200
            assert response.headers["content-type"] == "text/plain; charset=utf-8"
    
    def test_stream_no_rag_chain(self, client):
        """Test streaming when RAG chain is not initialized."""
        with patch('src.app.main.rag_chain', None):
            request_data = {"question": "Test question"}
            
            response = client.post("/query/stream", json=request_data)
            assert response.status_code == 503