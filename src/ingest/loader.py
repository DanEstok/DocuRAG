"""Document loader for PDF files."""

import os
from pathlib import Path
from typing import List

from langchain.document_loaders import PyPDFLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


class PDFLoader:
    """Load and process PDF documents."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        """Initialize the PDF loader.
        
        Args:
            chunk_size: Size of text chunks in tokens
            chunk_overlap: Overlap between chunks in tokens
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_pdf(self, file_path: str) -> List[Document]:
        """Load a single PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of document chunks
        """
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        # Add file name to metadata
        for doc in documents:
            doc.metadata["file_name"] = os.path.basename(file_path)
        
        return self.text_splitter.split_documents(documents)
    
    def load_directory(self, pdf_dir: str) -> List[Document]:
        """Load all PDF files from a directory.
        
        Args:
            pdf_dir: Directory containing PDF files
            
        Returns:
            List of all document chunks
        """
        pdf_path = Path(pdf_dir)
        if not pdf_path.exists():
            raise FileNotFoundError(f"Directory {pdf_dir} does not exist")
        
        all_documents = []
        pdf_files = list(pdf_path.glob("*.pdf"))
        
        if not pdf_files:
            raise ValueError(f"No PDF files found in {pdf_dir}")
        
        for pdf_file in pdf_files:
            print(f"Loading {pdf_file.name}...")
            documents = self.load_pdf(str(pdf_file))
            all_documents.extend(documents)
        
        print(f"Loaded {len(all_documents)} document chunks from {len(pdf_files)} PDF files")
        return all_documents