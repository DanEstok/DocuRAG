"""Setup script for development environment."""

import os
import sys
import subprocess
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from create_test_data import main as create_test_data


def run_command(command: str, description: str) -> bool:
    """Run a shell command and return success status.
    
    Args:
        command: Command to run
        description: Description for user
        
    Returns:
        True if successful, False otherwise
    """
    print(f"📋 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False


def setup_environment():
    """Set up development environment."""
    print("🚀 Setting up DocuRAG development environment...\n")
    
    # 1. Copy development environment file
    print("📋 Setting up environment configuration...")
    if not os.path.exists(".env"):
        if os.path.exists(".env.development"):
            import shutil
            shutil.copy(".env.development", ".env")
            print("✅ Copied .env.development to .env")
        else:
            print("❌ .env.development not found")
            return False
    else:
        print("✅ .env already exists")
    
    # 2. Create directories
    print("📋 Creating directories...")
    directories = ["data/dev", "data/test", "index/dev", "index/test", "tests/fixtures"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("✅ Directories created")
    
    # 3. Install dependencies
    if not run_command("pip install reportlab", "Installing reportlab for PDF generation"):
        return False
    
    # 4. Create test data
    print("📋 Creating test data...")
    try:
        create_test_data()
        print("✅ Test data created")
    except Exception as e:
        print(f"❌ Failed to create test data: {e}")
        return False
    
    # 5. Build development index
    print("📋 Building development index...")
    os.environ["ENVIRONMENT"] = "development"
    
    build_command = (
        "python src/ingest/build_index.py "
        "--pdf_dir data/dev "
        "--out index/dev "
        "--store faiss "
        "--chunk_size 500 "
        "--chunk_overlap 50"
    )
    
    if not run_command(build_command, "Building development index"):
        print("⚠️  Index build failed - this is normal if dependencies are missing")
        print("   You can build the index later with: python src/ingest/build_index.py --pdf_dir data/dev --out index/dev")
    
    # 6. Test the setup
    print("📋 Testing setup...")
    test_command = "python -c \"from src.app.main import app; print('✅ Import successful')\""
    
    if run_command(test_command, "Testing imports"):
        print("\n🎉 Development environment setup complete!")
        print("\n📖 Next steps:")
        print("   1. Start the development server: python src/app/main.py")
        print("   2. Visit http://localhost:8000/docs for API documentation")
        print("   3. Test the health endpoint: curl http://localhost:8000/healthz")
        print("   4. Try a query: curl -X POST http://localhost:8000/query -H 'Content-Type: application/json' -d '{\"question\": \"What is machine learning?\"}'")
        return True
    else:
        print("❌ Setup test failed")
        return False


def main():
    """Main entry point."""
    if setup_environment():
        sys.exit(0)
    else:
        print("\n❌ Setup failed. Please check the errors above and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()