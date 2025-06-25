# DocuRAG Ingestion Guide

## Overview

The ingestion pipeline processes PDF documents and creates searchable vector indices that power the RAG system. This guide covers how to prepare documents, run the ingestion process, and optimize performance.

## Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key
- PDF documents to process

### Basic Usage

```bash
# Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Run ingestion with default settings
python src/ingest/build_index.py --pdf_dir ./data --out ./index --store faiss

# Or using Docker
docker-compose run ingest
```

## Document Preparation

### Supported Formats
- **PDF files**: Primary supported format
- **Text quality**: OCR-scanned PDFs may have reduced accuracy
- **File size**: No hard limits, but larger files take longer to process

### Best Practices
1. **File naming**: Use descriptive filenames (included in metadata)
2. **Directory structure**: Organize PDFs in a single directory
3. **File quality**: Ensure PDFs are text-searchable, not just images
4. **Deduplication**: Remove duplicate documents before processing

### Document Structure
The system works best with:
- Well-structured documents with clear sections
- Consistent formatting and typography
- Proper page breaks and headers
- Minimal tables and complex layouts

## Ingestion Process

### Command Line Interface

```bash
python src/ingest/build_index.py [OPTIONS]

Options:
  --pdf_dir TEXT     Directory containing PDF files [required]
  --out TEXT         Output directory for the index [required]
  --store TEXT       Vector store type: faiss|chroma [default: faiss]
  --chunk_size INT   Chunk size in tokens [default: 1000]
  --chunk_overlap INT Chunk overlap in tokens [default: 100]
```

### Process Steps

1. **Document Loading**
   - Scan directory for PDF files
   - Load each PDF using PyPDFLoader
   - Extract text and metadata (page numbers, file names)

2. **Text Chunking**
   - Split documents into overlapping chunks
   - Preserve context across chunk boundaries
   - Maintain metadata for source tracking

3. **Embedding Generation**
   - Generate embeddings using OpenAI's text-embedding-ada-002
   - Process chunks in batches for efficiency
   - Handle rate limiting and retries

4. **Index Creation**
   - Store embeddings in vector database
   - Create searchable index structure
   - Persist to disk for later use

### Example Output

```
Loading document1.pdf...
Loading document2.pdf...
Loading document3.pdf...
Loaded 150 document chunks from 3 PDF files
Building faiss index...
Index saved to ./index
```

## Vector Store Options

### FAISS (Default)
- **Pros**: Fast similarity search, memory efficient, CPU-optimized
- **Cons**: No built-in persistence features
- **Best for**: Production deployments, large document collections

```bash
python src/ingest/build_index.py --pdf_dir ./data --out ./index --store faiss
```

### Chroma
- **Pros**: Built-in persistence, metadata filtering, easy to use
- **Cons**: Slower than FAISS for large collections
- **Best for**: Development, smaller document collections

```bash
python src/ingest/build_index.py --pdf_dir ./data --out ./index --store chroma
```

## Configuration Options

### Chunking Parameters

**Chunk Size (--chunk_size)**
- Default: 1000 tokens
- Smaller chunks: More precise retrieval, less context
- Larger chunks: More context, less precise retrieval
- Recommended range: 500-2000 tokens

**Chunk Overlap (--chunk_overlap)**
- Default: 100 tokens
- Purpose: Preserve context across chunk boundaries
- Recommended: 10-20% of chunk size

### Embedding Model
Currently uses OpenAI's `text-embedding-ada-002`:
- 1536 dimensions
- Cost: $0.0001 per 1K tokens
- Rate limit: 3,000 requests per minute

## Performance Optimization

### Processing Speed
1. **Batch processing**: Process multiple documents in parallel
2. **Rate limiting**: Respect OpenAI API limits
3. **Caching**: Avoid reprocessing unchanged documents
4. **Memory management**: Process large collections in batches

### Cost Optimization
1. **Deduplication**: Remove duplicate content before processing
2. **Preprocessing**: Clean documents to reduce token count
3. **Selective processing**: Only process relevant sections
4. **Monitoring**: Track token usage and costs

## Docker Usage

### Building the Image

```bash
docker build -f docker/Dockerfile.ingest -t docurag-ingest .
```

### Running Ingestion

```bash
# Using docker run
docker run -v $(pwd)/data:/app/data -v $(pwd)/index:/app/index \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  docurag-ingest \
  python src/ingest/build_index.py --pdf_dir ./data --out ./index

# Using docker-compose
docker-compose run ingest
```

## Troubleshooting

### Common Issues

**No PDF files found**
```
ValueError: No PDF files found in ./data
```
- Solution: Ensure PDF files exist in the specified directory
- Check file extensions (.pdf)

**OpenAI API key missing**
```
ValueError: OPENAI_API_KEY environment variable is required
```
- Solution: Set the environment variable
- Verify API key is valid and has sufficient credits

**Memory errors with large documents**
```
MemoryError: Unable to allocate array
```
- Solution: Reduce chunk size or process fewer documents at once
- Consider using a machine with more RAM

**Rate limiting errors**
```
RateLimitError: Rate limit exceeded
```
- Solution: The system includes automatic retries
- For large collections, consider processing in smaller batches

### Performance Issues

**Slow processing**
- Check internet connection for OpenAI API calls
- Verify PDF quality (OCR vs. native text)
- Consider using smaller chunk sizes

**Large index sizes**
- Review chunk size and overlap settings
- Remove unnecessary documents
- Consider document preprocessing

## Monitoring and Logging

### Progress Tracking
The ingestion process provides real-time feedback:
- Document loading progress
- Chunk count and statistics
- Embedding generation status
- Index creation and persistence

### Log Files
Enable detailed logging for troubleshooting:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Integration with API

### Automatic Refresh
The API includes a refresh endpoint for updating indices:

```bash
curl -X POST http://localhost:8000/refresh \
  -H "Content-Type: application/json" \
  -d '{"pdf_dir": "./new_documents"}'
```

### Index Validation
Verify index integrity after ingestion:
```python
from src.app.rag_chain import RAGChain

# Load and test the index
chain = RAGChain("./index", "faiss")
result = chain.query("test query")
```

## Best Practices

### Document Management
1. **Version control**: Track document versions and changes
2. **Backup**: Maintain backups of both documents and indices
3. **Validation**: Test indices after creation
4. **Documentation**: Keep records of ingestion parameters

### Production Deployment
1. **Automation**: Use CI/CD for regular index updates
2. **Monitoring**: Track ingestion success and performance
3. **Scaling**: Consider distributed processing for large collections
4. **Security**: Protect API keys and sensitive documents