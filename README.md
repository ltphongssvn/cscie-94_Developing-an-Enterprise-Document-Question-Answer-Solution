# README.md
# Railway Deployment Guide

## Prerequisites
- Railway account
- GitHub repository connected
- Cloudflare account with DNS access

## Step 1: Railway Setup

1. Go to railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select this repository
4. Railway auto-detects Dockerfile

## Step 2: Environment Variables

Add in Railway dashboard:
```
AZURE_OPENAI_ENDPOINT_SWEDEN=https://swedencentral.api.cognitive.microsoft.com/
AZURE_OPENAI_KEY_SWEDEN=<your-key>
AZURE_OPENAI_API_VERSION=2024-08-01-preview
```

## Step 3: Generate Domain

Railway provides: `https://<project>.railway.app`

## Step 4: Cloudflare DNS

1. Log into Cloudflare
2. Select domain: thanhphongle.net
3. Add CNAME record:
   - Name: `aoai-fine-tuning`
   - Target: `<project>.railway.app`
   - Proxy: Enabled (orange cloud)

## Step 5: Custom Domain in Railway

1. Railway Settings → Domains
2. Add: `aoai-fine-tuning.thanhphongle.net`
3. Wait for SSL provisioning (~5 min)

## Verification

- API: `https://aoai-fine-tuning.thanhphongle.net/api`
- UI: `https://aoai-fine-tuning.thanhphongle.net/`

## Architecture
```
User → Cloudflare DNS → Railway
                         ├─ FastAPI (/api)
                         └─ React (/)
```
