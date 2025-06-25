"""Test script to verify the setup works correctly."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

def test_imports():
    """Test that all imports work correctly."""
    print("🧪 Testing imports...")
    
    try:
        from app.config import settings
        print("✅ Config import successful")
        
        from app.mock_llm import MockEmbeddings, MockLLM
        print("✅ Mock LLM import successful")
        
        from app.schemas import QueryRequest, QueryResponse
        print("✅ Schemas import successful")
        
        from ingest.loader import PDFLoader
        print("✅ Loader import successful")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_mock_llm():
    """Test mock LLM functionality."""
    print("🧪 Testing mock LLM...")
    
    try:
        from app.mock_llm import MockEmbeddings, MockLLM
        
        # Test embeddings
        embeddings = MockEmbeddings()
        test_embedding = embeddings.embed_query("test query")
        assert len(test_embedding) == 1536
        print("✅ Mock embeddings working")
        
        # Test LLM
        llm = MockLLM(response_delay=0.1)
        response = llm._call("What is machine learning?")
        assert len(response) > 0
        print("✅ Mock LLM working")
        
        return True
    except Exception as e:
        print(f"❌ Mock LLM test failed: {e}")
        return False


def test_config():
    """Test configuration system."""
    print("🧪 Testing configuration...")
    
    try:
        from app.config import settings
        
        # Test environment detection
        print(f"Environment: {settings.environment}")
        print(f"Should use mock LLM: {settings.should_use_mock_llm}")
        print(f"Index path: {settings.index_path}")
        print(f"Vector store: {settings.vector_store}")
        
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False


def test_development_mode():
    """Test development mode setup."""
    print("🧪 Testing development mode...")
    
    try:
        # Set development environment
        os.environ["ENVIRONMENT"] = "development"
        
        # Reload settings
        from app.config import Settings
        dev_settings = Settings()
        
        assert dev_settings.is_development
        assert dev_settings.should_use_mock_llm
        print("✅ Development mode working")
        
        return True
    except Exception as e:
        print(f"❌ Development mode test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 Running DocuRAG setup tests...\n")
    
    tests = [
        test_imports,
        test_config,
        test_mock_llm,
        test_development_mode
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}\n")
    
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Setup is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the setup.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)