# docs/RAILWAY_DEPLOYMENT.md
# Full path: /docs/RAILWAY_DEPLOYMENT.md

# Railway Deployment Guide

## Prerequisites
- Railway account: https://railway.app
- GitHub repository connected
- Cloudflare account for DNS

## Backend Deployment Steps

### 1. Create Railway Project
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Create project
railway init
```

### 2. Set Environment Variables
In Railway dashboard, add:
```
AZURE_OPENAI_ENDPOINT=https://openai-docqa-9534.openai.azure.com/
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME=text-embedding-ada-002
AZURE_SEARCH_ENDPOINT=https://search-docqa-24180.search.windows.net
AZURE_SEARCH_API_KEY=your-key
AZURE_SEARCH_INDEX_NAME=documents-index
```

### 3. Deploy
- Connect GitHub repository
- Railway auto-deploys from Dockerfile
- Get public URL: `https://your-app.railway.app`

## Frontend Deployment

### 1. Build React App
```bash
cd frontend
npm run build
```

### 2. Deploy to Vercel/Netlify
```bash
# Vercel
vercel --prod

# Or Netlify
netlify deploy --prod --dir=build
```

### 3. Set Environment Variable
```
REACT_APP_API_URL=https://your-railway-app.railway.app
```

## Cloudflare DNS Setup

### 1. Add CNAME Record
```
Type: CNAME
Name: enterprise-document-question-answer-solution
Target: your-app.railway.app
Proxy: Enabled (Orange cloud)
```

### 2. Custom Domain in Railway
- Go to Railway project settings
- Add custom domain: enterprise-document-question-answer-solution.thanhphongle.net
- Verify DNS propagation

## Testing
```bash
curl https://enterprise-document-question-answer-solution.thanhphongle.net/health
```

## Monitoring
- Railway dashboard: Logs and metrics
- Cloudflare Analytics: Traffic and performance
