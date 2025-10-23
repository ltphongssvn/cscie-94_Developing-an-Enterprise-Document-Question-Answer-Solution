# README.md
# Full path: /README.md

# CSCIE-94 Developing an Enterprise Document Question-Answer Solution

Azure OpenAI-powered document Q&A system using Cognitive Search for enterprise unstructured data retrieval.

## Features

- Azure OpenAI integration for embeddings and LLM
- Azure Cognitive Search vector store
- Document processing (PDF, DOCX, TXT)
- LangChain-based retrieval QA chain
- Pre-commit hooks for code quality
- Automated GitFlow branching

## Quick Start
```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with Azure credentials

# Run application
python src/document_qa.py
```

## Project Structure
```
.
├── src/
│   └── document_qa.py      # Main application
├── data/                   # Document storage
├── docs/
│   ├── ARCHITECTURE.md     # System architecture
│   └── SETUP.md           # Setup instructions
├── tests/
│   └── test_document_qa.py # Unit tests
├── requirements.txt        # Dependencies
└── .env.example           # Environment template
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Setup Guide](docs/SETUP.md)

## Technology Stack

- Python 3.13
- Azure OpenAI
- Azure Cognitive Search
- LangChain
- UV Package Manager

## License

MIT
