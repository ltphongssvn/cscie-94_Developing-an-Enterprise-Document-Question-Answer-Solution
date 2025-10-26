# /Dockerfile
# Multi-stage build for FastAPI backend + React frontend
FROM node:22-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim
WORKDIR /app
# Install backend dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Copy backend
COPY backend/ ./backend/
# Copy frontend build
COPY --from=frontend-build /app/frontend/build ./frontend/build

EXPOSE 8000
# Use shell form to allow PORT variable expansion
CMD uvicorn backend.api:app --host 0.0.0.0 --port ${PORT:-8000}
