# fine_tuning/GET_OPENAI_KEY.md
# How to Get OpenAI API Key

## Quick Steps:
1. Go to https://platform.openai.com/api-keys
2. Sign up/Log in with your account
3. Click "Create new secret key"
4. Copy the key (starts with sk-)
5. Run: ./fine_tuning/add_openai_key.sh
6. Paste the key when prompted

## Cost Note:
- Fine-tuning costs ~$0.008/1K tokens
- Your dataset: ~54KB = ~$0.50 for training

## After Adding Key:
1. python fine_tuning/upload_to_openai.py
2. Update file IDs in create_finetune_openai_complete.py
3. python fine_tuning/create_finetune_openai_complete.py
