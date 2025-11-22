#!/bin/bash

# set -e  # Exit on any error

echo "Applying Alembic migrations..."

uv run alembic upgrade head

echo "Starting FastAPI server ..."
exec uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload