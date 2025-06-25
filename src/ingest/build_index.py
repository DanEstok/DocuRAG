"""Build vector index from PDF documents."""

import argparse
import os
import sys
from pathlib import Path
from typing import Literal

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS, Chroma

from .loader import PDFLoader
from app.config import settings
from app.mock_llm import MockEmbeddings


def build_index(
    pdf_dir: str,
    output_dir: str,
    store_type: Literal["faiss", "chroma"] = "faiss",
    chunk_size: int = 1000,
    chunk_overlap: int = 100
) -> None:
    """Build vector index from PDF documents.
    
    Args:
        pdf_dir: Directory containing PDF files
        output_dir: Directory to save the index
        store_type: Type of vector store (faiss or chroma)
        chunk_size: Size of text chunks in tokens
        chunk_overlap: Overlap between chunks in tokens
    """
    # Validate configuration
    use_mock = settings.should_use_mock_llm
    if not use_mock and not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is required for production mode")
    
    # Load documents
    loader = PDFLoader(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    documents = loader.load_directory(pdf_dir)
    
    # Initialize embeddings
    if use_mock:
        embeddings = MockEmbeddings()
        print("Using mock embeddings for development")
    else:
        embeddings = OpenAIEmbeddings()
        print("Using OpenAI embeddings for production")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Build vector store
    print(f"Building {store_type} index...")
    if store_type == "faiss":
        vectorstore = FAISS.from_documents(documents, embeddings)
        vectorstore.save_local(str(output_path))
    elif store_type == "chroma":
        vectorstore = Chroma.from_documents(
            documents, 
            embeddings, 
            persist_directory=str(output_path)
        )
        vectorstore.persist()
    else:
        raise ValueError(f"Unsupported store type: {store_type}")
    
    print(f"Index saved to {output_dir}")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Build vector index from PDF documents")
    parser.add_argument("--pdf_dir", required=True, help="Directory containing PDF files")
    parser.add_argument("--out", required=True, help="Output directory for the index")
    parser.add_argument(
        "--store", 
        choices=["faiss", "chroma"], 
        default="faiss",
        help="Vector store type"
    )
    parser.add_argument("--chunk_size", type=int, default=1000, help="Chunk size in tokens")
    parser.add_argument("--chunk_overlap", type=int, default=100, help="Chunk overlap in tokens")
    
    args = parser.parse_args()
    
    build_index(
        pdf_dir=args.pdf_dir,
        output_dir=args.out,
        store_type=args.store,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap
    )


if __name__ == "__main__":
    main()