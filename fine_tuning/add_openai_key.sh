#!/bin/bash
# fine_tuning/add_openai_key.sh
# Script to add OpenAI API key to .env file

echo "Enter your OpenAI API key (starts with sk-):"
read -r api_key

if [[ ! "$api_key" =~ ^sk- ]]; then
    echo "Error: Invalid key format. OpenAI keys start with 'sk-'"
    exit 1
fi

if grep -q "OPENAI_API_KEY" .env 2>/dev/null; then
    sed -i "s/^OPENAI_API_KEY=.*/OPENAI_API_KEY=$api_key/" .env
else
    echo "OPENAI_API_KEY=$api_key" >> .env
fi

echo "Added OPENAI_API_KEY to .env"
echo "Next: Run python fine_tuning/upload_to_openai.py"
