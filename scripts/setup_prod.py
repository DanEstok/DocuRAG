"""Setup script for production environment."""

import os
import sys
import subprocess
from pathlib import Path


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


def validate_production_config():
    """Validate production configuration."""
    print("📋 Validating production configuration...")
    
    # Check for required environment variables
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("   Please set these variables before running in production mode.")
        return False
    
    print("✅ Production configuration validated")
    return True


def setup_production():
    """Set up production environment."""
    print("🚀 Setting up DocuRAG production environment...\n")
    
    # 1. Set production environment
    os.environ["ENVIRONMENT"] = "production"
    
    # 2. Copy production environment file if needed
    print("📋 Setting up environment configuration...")
    if not os.path.exists(".env"):
        if os.path.exists(".env.production"):
            print("⚠️  .env.production found but .env doesn't exist")
            print("   Please copy .env.production to .env and configure your API keys")
            return False
        else:
            print("❌ No environment configuration found")
            return False
    
    # 3. Validate configuration
    if not validate_production_config():
        return False
    
    # 4. Create directories
    print("📋 Creating directories...")
    directories = ["data", "index", "logs"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("✅ Directories created")
    
    # 5. Check for PDF documents
    data_dir = Path("data")
    pdf_files = list(data_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("⚠️  No PDF files found in data/ directory")
        print("   Please add PDF documents to data/ before building the index")
        return False
    
    print(f"✅ Found {len(pdf_files)} PDF files")
    
    # 6. Build production index
    print("📋 Building production index...")
    
    build_command = (
        "python src/ingest/build_index.py "
        "--pdf_dir data "
        "--out index "
        "--store faiss "
        "--chunk_size 1000 "
        "--chunk_overlap 100"
    )
    
    if not run_command(build_command, "Building production index"):
        return False
    
    # 7. Test the setup
    print("📋 Testing production setup...")
    test_command = "python -c \"from src.app.config import settings; settings.validate_production_config(); print('✅ Production config valid')\""
    
    if not run_command(test_command, "Validating production configuration"):
        return False
    
    print("\n🎉 Production environment setup complete!")
    print("\n📖 Next steps:")
    print("   1. Start the production server: python src/app/main.py")
    print("   2. Or use Docker: docker-compose up")
    print("   3. Monitor logs and performance")
    print("   4. Set up reverse proxy (nginx/apache) for HTTPS")
    print("   5. Configure monitoring and alerting")
    
    return True


def main():
    """Main entry point."""
    if setup_production():
        sys.exit(0)
    else:
        print("\n❌ Production setup failed. Please check the errors above and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()