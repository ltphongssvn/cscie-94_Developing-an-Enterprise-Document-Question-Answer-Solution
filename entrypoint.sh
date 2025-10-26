#!/bin/sh
# /entrypoint.sh

# Railway should provide PORT, but fallback to 8000 if not set
if [ -z "$PORT" ]; then
    export PORT=8000
    echo "PORT not set, defaulting to $PORT"
fi

echo "Starting server on port $PORT"
exec uvicorn backend.api:app --host 0.0.0.0 --port $PORT
