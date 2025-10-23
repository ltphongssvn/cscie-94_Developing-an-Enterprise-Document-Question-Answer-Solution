# docs/SETUP.md
# Full path: /docs/SETUP.md

# Setup Guide

## Prerequisites

1. **Azure Account**: Active subscription with Azure OpenAI access
2. **Python**: 3.8+ installed
3. **UV Package Manager**: Installed

## Azure Resources Setup

### 1. Azure OpenAI Service
```bash
# Create resource group
az group create --name rg-docqa --location eastus

# Create Azure OpenAI resource
az cognitiveservices account create \
  --name openai-docqa \
  --resource-group rg-docqa \
  --kind OpenAI \
  --sku S0 \
  --location eastus
```

### 2. Deploy Models

Deploy these models in Azure OpenAI Studio:
- **GPT-4**: For answer generation
- **text-embedding-ada-002**: For embeddings

### 3. Azure Cognitive Search
```bash
# Create Azure Cognitive Search
az search service create \
  --name search-docqa \
  --resource-group rg-docqa \
  --sku standard \
  --location eastus
```

## Local Setup

### 1. Clone and Install
```bash
git clone <your-repo-url>
cd cscie-94_Developing-an-Enterprise-Document-Question-Answer-Solution
git checkout feature/oct-23-95-days-to-CSCIE-94
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your Azure credentials
```

### 3. Add Documents

Place PDF files in `data/` directory.

### 4. Run Application
```bash
python src/document_qa.py
```

## Configuration

Required `.env` variables:
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_API_VERSION`
- `AZURE_OPENAI_DEPLOYMENT_NAME`
- `AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME`
- `AZURE_SEARCH_ENDPOINT`
- `AZURE_SEARCH_API_KEY`
- `AZURE_SEARCH_INDEX_NAME`
