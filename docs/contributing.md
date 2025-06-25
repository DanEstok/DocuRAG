# Contributing to DocuRAG

## Welcome

Thank you for your interest in contributing to DocuRAG! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

### Our Pledge

We are committed to making participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.11+
- Git
- Docker and Docker Compose
- OpenAI API key for testing

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone https://github.com/your-username/DocuRAG.git
cd DocuRAG
```

3. Add the upstream repository:
```bash
git remote add upstream https://github.com/original-owner/DocuRAG.git
```

## Development Setup

### Local Environment

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

3. Set up environment variables:
```bash
export OPENAI_API_KEY="your-test-api-key"
export VECTOR_STORE="faiss"
```

4. Create test data:
```bash
mkdir -p data
# Add sample PDF files for testing
```

### Docker Development

1. Build development images:
```bash
docker-compose -f docker-compose.dev.yml build
```

2. Run development environment:
```bash
docker-compose -f docker-compose.dev.yml up
```

### Pre-commit Hooks

Install pre-commit hooks to ensure code quality:
```bash
pip install pre-commit
pre-commit install
```

## Contributing Guidelines

### Types of Contributions

We welcome several types of contributions:

1. **Bug Reports**: Help us identify and fix issues
2. **Feature Requests**: Suggest new functionality
3. **Code Contributions**: Implement features or fix bugs
4. **Documentation**: Improve or add documentation
5. **Testing**: Add or improve test coverage
6. **Performance**: Optimize existing functionality

### Contribution Workflow

1. **Check existing issues**: Look for existing issues or discussions
2. **Create an issue**: For new features or bugs, create an issue first
3. **Fork and branch**: Create a feature branch from main
4. **Develop**: Make your changes following our standards
5. **Test**: Ensure all tests pass and add new tests
6. **Document**: Update documentation as needed
7. **Submit**: Create a pull request

## Code Standards

### Python Style Guide

We follow PEP 8 with some modifications enforced by our tools:

- **Line length**: 88 characters (Black default)
- **Import sorting**: Use isort
- **Type hints**: Required for all public functions
- **Docstrings**: Google style for all public functions and classes

### Code Formatting

We use automated formatting tools:

```bash
# Format code with Black
black src/ tests/ scripts/

# Sort imports with isort
isort src/ tests/ scripts/

# Lint with Ruff
ruff check src/ tests/ scripts/

# Type checking with mypy
mypy src/
```

### Example Code Style

```python
"""Module docstring describing the purpose."""

from typing import List, Optional, Dict, Any
import os
from pathlib import Path

from langchain.schema import Document
from pydantic import BaseModel, Field


class ExampleClass:
    """Class docstring describing the class.
    
    Args:
        param1: Description of parameter
        param2: Description of parameter
    """
    
    def __init__(self, param1: str, param2: Optional[int] = None):
        self.param1 = param1
        self.param2 = param2
    
    def public_method(self, input_data: List[str]) -> Dict[str, Any]:
        """Public method with proper docstring.
        
        Args:
            input_data: List of input strings to process
            
        Returns:
            Dictionary containing processed results
            
        Raises:
            ValueError: If input_data is empty
        """
        if not input_data:
            raise ValueError("input_data cannot be empty")
        
        return {"processed": len(input_data)}
    
    def _private_method(self) -> None:
        """Private method (minimal docstring acceptable)."""
        pass
```

### Pydantic Models

```python
class RequestModel(BaseModel):
    """Request model with proper validation."""
    
    question: str = Field(..., description="The question to ask")
    max_tokens: Optional[int] = Field(
        default=1000, 
        ge=1, 
        le=4000, 
        description="Maximum tokens in response"
    )
    
    class Config:
        """Pydantic configuration."""
        extra = "forbid"
        validate_assignment = True
```

## Testing

### Test Structure

```
tests/
├── unit/
│   ├── test_ingest/
│   │   ├── test_loader.py
│   │   └── test_build_index.py
│   └── test_app/
│       ├── test_rag_chain.py
│       └── test_main.py
├── integration/
│   ├── test_api_integration.py
│   └── test_end_to_end.py
└── fixtures/
    ├── sample.pdf
    └── test_data.json
```

### Writing Tests

```python
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from src.app.main import app


class TestQueryEndpoint:
    """Test class for query endpoint."""
    
    @pytest.fixture
    def client(self):
        """Test client fixture."""
        return TestClient(app)
    
    @pytest.fixture
    def mock_rag_chain(self):
        """Mock RAG chain fixture."""
        mock_chain = MagicMock()
        mock_chain.query.return_value = ("test answer", [])
        return mock_chain
    
    def test_query_success(self, client, mock_rag_chain):
        """Test successful query."""
        with patch('src.app.main.rag_chain', mock_rag_chain):
            response = client.post("/query", json={"question": "test"})
            assert response.status_code == 200
            data = response.json()
            assert "answer" in data
    
    @pytest.mark.parametrize("question,expected", [
        ("", 422),  # Empty question
        ("valid question", 200),  # Valid question
    ])
    def test_query_validation(self, client, question, expected):
        """Test query validation."""
        response = client.post("/query", json={"question": question})
        assert response.status_code == expected
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_app.py

# Run with verbose output
pytest -v

# Run only fast tests (exclude slow integration tests)
pytest -m "not slow"
```

### Test Markers

Use pytest markers to categorize tests:

```python
import pytest

@pytest.mark.unit
def test_unit_function():
    """Fast unit test."""
    pass

@pytest.mark.integration
def test_integration():
    """Integration test."""
    pass

@pytest.mark.slow
def test_slow_operation():
    """Slow test that hits external APIs."""
    pass
```

## Documentation

### Documentation Types

1. **Code Documentation**: Docstrings and inline comments
2. **API Documentation**: Automatically generated from FastAPI
3. **User Documentation**: Markdown files in `docs/`
4. **README**: Project overview and quick start

### Writing Documentation

- Use clear, concise language
- Include code examples
- Keep documentation up to date with code changes
- Use proper Markdown formatting

### Building Documentation

```bash
# Generate API documentation
python -c "
import json
from src.app.main import app
with open('docs/openapi.json', 'w') as f:
    json.dump(app.openapi(), f, indent=2)
"

# Serve documentation locally
python -m http.server 8080 --directory docs/
```

## Pull Request Process

### Before Submitting

1. **Sync with upstream**:
```bash
git fetch upstream
git checkout main
git merge upstream/main
```

2. **Create feature branch**:
```bash
git checkout -b feature/your-feature-name
```

3. **Make changes and commit**:
```bash
git add .
git commit -m "feat: add new feature description"
```

4. **Run tests and linting**:
```bash
pytest
ruff check src/ tests/
black --check src/ tests/
```

5. **Push to your fork**:
```bash
git push origin feature/your-feature-name
```

### Pull Request Template

When creating a pull request, include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Updated documentation

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Commit Message Format

Use conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(api): add streaming query endpoint
fix(ingest): handle empty PDF directories
docs(readme): update installation instructions
test(app): add integration tests for query endpoint
```

## Issue Reporting

### Bug Reports

When reporting bugs, include:

1. **Environment information**:
   - Python version
   - Operating system
   - Docker version (if applicable)
   - Relevant package versions

2. **Steps to reproduce**:
   - Minimal code example
   - Input data (if applicable)
   - Expected vs. actual behavior

3. **Error messages**:
   - Full stack traces
   - Log output
   - Screenshots (if applicable)

### Feature Requests

When requesting features, include:

1. **Problem description**: What problem does this solve?
2. **Proposed solution**: How should it work?
3. **Alternatives considered**: Other approaches you've considered
4. **Additional context**: Any other relevant information

### Issue Templates

Use our issue templates:

- **Bug Report**: For reporting bugs
- **Feature Request**: For suggesting new features
- **Documentation**: For documentation improvements
- **Question**: For asking questions

## Development Guidelines

### Adding New Features

1. **Design first**: Create an issue to discuss the design
2. **Start small**: Break large features into smaller PRs
3. **Test thoroughly**: Add comprehensive tests
4. **Document**: Update relevant documentation
5. **Consider backwards compatibility**: Avoid breaking changes

### Code Review Process

1. **Self-review**: Review your own code first
2. **Automated checks**: Ensure CI passes
3. **Peer review**: Address reviewer feedback
4. **Maintainer review**: Final review by maintainers

### Release Process

1. **Version bumping**: Follow semantic versioning
2. **Changelog**: Update CHANGELOG.md
3. **Testing**: Comprehensive testing before release
4. **Documentation**: Update version-specific docs

## Getting Help

### Communication Channels

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Discord/Slack**: Real-time chat (if available)

### Mentorship

New contributors can:
- Look for "good first issue" labels
- Ask for mentorship in issues
- Join contributor onboarding sessions

## Recognition

Contributors are recognized through:
- GitHub contributor graphs
- CONTRIBUTORS.md file
- Release notes acknowledgments
- Community highlights

Thank you for contributing to DocuRAG! 🚀