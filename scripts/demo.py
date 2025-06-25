"""Demo script showing DocuRAG capabilities."""

import os
import sys
import time
import requests
import subprocess
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))


def start_server():
    """Start the development server."""
    print("🚀 Starting DocuRAG development server...")
    
    # Set development environment
    os.environ["ENVIRONMENT"] = "development"
    
    # Start server in background
    try:
        process = subprocess.Popen([
            sys.executable, "src/app/main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(5)
        
        return process
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None


def test_api():
    """Test the API endpoints."""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing API endpoints...\n")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/healthz", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data['status']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test query endpoint
    try:
        query_data = {
            "question": "What is machine learning and how does it work?"
        }
        
        print("📝 Sending query: 'What is machine learning and how does it work?'")
        response = requests.post(
            f"{base_url}/query", 
            json=query_data, 
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Query successful!")
            print(f"📄 Answer: {data['answer'][:200]}...")
            print(f"📚 Sources: {len(data['sources'])} documents")
            
            if data['sources']:
                source = data['sources'][0]
                print(f"   - File: {source['file_name']}")
                print(f"   - Excerpt: {source['excerpt'][:100]}...")
        else:
            print(f"❌ Query failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Query error: {e}")
        return False
    
    # Test conversational query
    try:
        conv_data = {
            "question": "Can you explain that in simpler terms?",
            "chat_history": [
                ["What is machine learning?", "Machine learning is a subset of AI..."]
            ]
        }
        
        print("\n💬 Testing conversational query...")
        response = requests.post(
            f"{base_url}/query", 
            json=conv_data, 
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Conversational query successful!")
            print(f"📄 Answer: {data['answer'][:200]}...")
        else:
            print(f"❌ Conversational query failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Conversational query error: {e}")
    
    return True


def show_api_docs():
    """Show information about API documentation."""
    print("\n📖 API Documentation:")
    print("   - Swagger UI: http://localhost:8000/docs")
    print("   - ReDoc: http://localhost:8000/redoc")
    print("   - OpenAPI JSON: http://localhost:8000/openapi.json")


def show_example_commands():
    """Show example curl commands."""
    print("\n🔧 Example Commands:")
    
    print("\n# Health check")
    print("curl http://localhost:8000/healthz")
    
    print("\n# Simple query")
    print("""curl -X POST http://localhost:8000/query \\
  -H "Content-Type: application/json" \\
  -d '{"question": "What are the main topics in the documents?"}'""")
    
    print("\n# Conversational query")
    print("""curl -X POST http://localhost:8000/query \\
  -H "Content-Type: application/json" \\
  -d '{
    "question": "Can you elaborate on that?",
    "chat_history": [
      ["What is AI?", "AI is artificial intelligence..."]
    ]
  }'""")
    
    print("\n# Refresh index")
    print("""curl -X POST http://localhost:8000/refresh \\
  -H "Content-Type: application/json" \\
  -d '{"pdf_dir": "data/dev"}'""")


def main():
    """Run the demo."""
    print("🎯 DocuRAG Demo\n")
    print("This demo will:")
    print("1. Start the development server with mock LLM")
    print("2. Test the API endpoints")
    print("3. Show you how to interact with the system\n")
    
    input("Press Enter to continue...")
    
    # Start server
    server_process = start_server()
    if not server_process:
        print("❌ Failed to start server")
        return False
    
    try:
        # Test API
        if test_api():
            print("\n🎉 Demo successful!")
            
            # Show additional information
            show_api_docs()
            show_example_commands()
            
            print("\n🔄 The server is still running. You can:")
            print("   - Visit http://localhost:8000/docs to explore the API")
            print("   - Try the example commands above")
            print("   - Modify the test data in data/dev/")
            print("   - Switch to production mode with real OpenAI API")
            
            print("\nPress Ctrl+C to stop the server")
            
            # Keep server running
            try:
                server_process.wait()
            except KeyboardInterrupt:
                print("\n👋 Stopping server...")
                server_process.terminate()
                server_process.wait()
        else:
            print("❌ Demo failed")
            server_process.terminate()
            return False
    
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted")
        server_process.terminate()
        server_process.wait()
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)