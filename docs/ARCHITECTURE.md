# docs/ARCHITECTURE.md
# Full path: /docs/ARCHITECTURE.md

# Architecture Design

## Overview
Enterprise Document Q&A solution using Azure OpenAI and Azure Cognitive Search for unstructured document retrieval.

## Components

### Azure OpenAI Service
- **Embeddings**: Convert text to vectors
- **LLM**: Generate answers from context

### Azure Cognitive Search
- **Vector Store**: Store document embeddings
- **Similarity Search**: Retrieve top-k relevant passages

## Process Flow

1. **Document Ingestion**
   - Load documents (PDF, DOCX)
   - Split into chunks (1000 chars, 200 overlap)

2. **Embedding Generation**
   - Transform chunks → embeddings via Azure OpenAI

3. **Vector Storage**
   - Upsert embeddings to Azure Cognitive Search

4. **Query Processing**
   - User submits question
   - Generate query embedding
   - Vector search retrieves top-k passages

5. **Answer Generation**
   - Passages provided as context
   - Azure OpenAI generates answer

## Technology Stack
- Python 3.8+
- LangChain
- Azure OpenAI
- Azure Cognitive Search
