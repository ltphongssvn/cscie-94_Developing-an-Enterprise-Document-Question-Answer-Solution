# fine_tuning/AZURE_OPENAI_SETUP.md
# Option 1: Azure OpenAI Resource Setup

## Prerequisites Check
- Azure subscription with OpenAI access
- Resource group in supported region

## Provisioning Steps
1. Azure Portal: https://portal.azure.com
2. Create resource → Search "Azure OpenAI"
3. Select Azure OpenAI (NOT Cognitive Services)
4. Configure:
   - Region: East US, West Europe, or Sweden Central
   - Name: your-unique-name
   - Pricing: S0

## Post-Approval (24-48hr wait)
Update .env:
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com/
AZURE_OPENAI_KEY=your-new-key

## Status
Current: Cognitive Services (no fine-tuning)
Required: Azure OpenAI Service
Alternative: OpenAI API (✓ Already working - job ftjob-7pc0kvPb7uefsGQif7o1WLm6)
