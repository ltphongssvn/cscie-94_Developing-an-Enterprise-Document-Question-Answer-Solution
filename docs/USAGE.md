# docs/USAGE.md
# Full path: /docs/USAGE.md

# Usage Guide

## Running the Application

### Interactive Mode
```bash
python src/cli.py --interactive
```

### Single Query
```bash
python src/cli.py --query "What destinations are included?"
```

### Custom Data Directory
```bash
python src/cli.py --data-dir /path/to/docs --interactive
```

## Validate Configuration
```bash
python src/config_validator.py
```

## Running Tests
```bash
pytest tests/ -v
```

## Azure Deployment
```bash
./scripts/deploy.sh
```

## Example Queries

- "What are the accommodation options?"
- "What is included in the package price?"
- "What are the visa requirements?"
- "How long is the trip?"
- "What activities are planned?"

## Troubleshooting

### Missing Environment Variables
- Check `.env` file exists
- Run `python src/config_validator.py`

### Import Errors
- Activate virtual environment: `source .venv/bin/activate`
- Reinstall: `uv pip install -r requirements.txt`

### No Documents Found
- Verify files in `data/` directory
- Check supported formats: PDF, TXT, DOCX

### Azure Connection Errors
- Verify endpoints and keys
- Check Azure resource status
- Ensure models are deployed
