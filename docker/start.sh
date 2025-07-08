#!/bin/bash

echo "🟡 Waiting for PostgreSQL to be ready..."
while ! nc -z postgres 5432; do
  sleep 1
done

echo "✅ PostgreSQL is up. Running Alembic migrations..."
alembic upgrade head

echo "🚀 Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000