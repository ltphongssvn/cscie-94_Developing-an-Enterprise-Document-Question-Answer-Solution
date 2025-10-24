# docs/CLOUD_DEPLOYMENT.md
# Full path: /docs/CLOUD_DEPLOYMENT.md

# Cloud Deployment Guide

## Deployed Azure Resources

### Resource Group
- Name: `rg-docqa`
- Location: East US

### Azure OpenAI
- Name: `openai-docqa-9534`
- Endpoint: `https://openai-docqa-9534.openai.azure.com/`
- Models Deployed:
  - `text-embedding-ada-002` (version 2)
  - `gpt-4` (turbo-2024-04-09)

### Azure Cognitive Search
- Name: `search-docqa-24180`
- Endpoint: `https://search-docqa-24180.search.windows.net`
- Index: `documents-index`

## Application Status
✅ Fully operational and tested

## Test Results
```
Query: "What are the main destinations?"
Answer: Bangkok, Chiang Mai (Thailand), Hanoi (Vietnam), Siem Reap (Cambodia)

Query: "What is included in the package?"
Answer: Domestic flights, 4-star hotels, breakfast, guided tours, transfers, entrance fees

Query: "What vaccinations are recommended?"
Answer: Hepatitis A/B, Typhoid
```

## Access Application
Repository: https://github.com/ltphongssvn/cscie-94_Developing-an-Enterprise-Document-Question-Answer-Solution

## Cost Estimates
- Azure OpenAI: ~$0.10/1K tokens (GPT-4)
- Embeddings: ~$0.0001/1K tokens
- Search: ~$250/month (Standard tier)

## Cleanup
To delete all resources:
```bash
az group delete --name rg-docqa --yes --no-wait
```
