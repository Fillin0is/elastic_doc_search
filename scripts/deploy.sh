#!/bin/bash
set -e

PROJECT_DIR="$HOME/elastic_doc_search"
REPO_URL="https://github.com/Fillin0is/elastic_doc_search"

cd "$PROJECT_DIR" || exit 1

echo "=== Pulling latest code ==="
git pull origin main

echo "=== Activating venv ==="
source venv/bin/activate

echo "=== Installing dependencies ==="
pip install -r requirements.txt --quiet

echo "=== Restarting Docker containers ==="
cd compose
docker compose -f server1.yml down
docker compose -f server1.yml up -d

echo "=== Done! ==="
docker compose -f server1.yml ps
