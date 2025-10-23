#!/bin/bash
# scripts/deploy.sh
# Full path: /scripts/deploy.sh

set -e

echo "======================================"
echo "Azure OpenAI Document Q&A Deployment"
echo "======================================"

# Variables
RESOURCE_GROUP="rg-docqa"
LOCATION="eastus"
OPENAI_NAME="openai-docqa-$RANDOM"
SEARCH_NAME="search-docqa-$RANDOM"

echo -e "\n1. Creating Resource Group..."
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION

echo -e "\n2. Creating Azure OpenAI Service..."
az cognitiveservices account create \
    --name $OPENAI_NAME \
    --resource-group $RESOURCE_GROUP \
    --kind OpenAI \
    --sku S0 \
    --location $LOCATION

echo -e "\n3. Creating Azure Cognitive Search..."
az search service create \
    --name $SEARCH_NAME \
    --resource-group $RESOURCE_GROUP \
    --sku standard \
    --location $LOCATION

echo -e "\n4. Retrieving Keys..."
OPENAI_KEY=$(az cognitiveservices account keys list \
    --name $OPENAI_NAME \
    --resource-group $RESOURCE_GROUP \
    --query key1 -o tsv)

SEARCH_KEY=$(az search admin-key show \
    --service-name $SEARCH_NAME \
    --resource-group $RESOURCE_GROUP \
    --query primaryKey -o tsv)

echo -e "\n======================================"
echo "Deployment Complete!"
echo "======================================"
echo -e "\nAzure OpenAI:"
echo "  Name: $OPENAI_NAME"
echo "  Endpoint: https://$OPENAI_NAME.openai.azure.com/"
echo -e "\nAzure Search:"
echo "  Name: $SEARCH_NAME"
echo "  Endpoint: https://$SEARCH_NAME.search.windows.net"
echo -e "\nNext Steps:"
echo "1. Deploy models in Azure OpenAI Studio:"
echo "   - gpt-4 (or gpt-35-turbo)"
echo "   - text-embedding-ada-002"
echo "2. Update .env file with endpoints and keys"
echo "======================================"
