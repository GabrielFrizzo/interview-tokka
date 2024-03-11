#! /usr/bin/env bash
set -e

sleep 4 # wait for the database to start
poetry run python src/alembic/main.py
echo "Tables created. Starting server..."
poetry run uvicorn src.api.main:app --host 0.0.0.0 --port 80 --reload
