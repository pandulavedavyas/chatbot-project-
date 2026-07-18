#!/bin/bash

echo "=== Installing Python dependencies ==="
pip install -r backend/requirements.txt

echo "=== Installing Node.js dependencies ==="
cd frontend && npm install

echo "=== Building React frontend ==="
npm run build

echo "=== Copying build output to backend/static ==="
rm -rf ../backend/static
mkdir -p ../backend/static
cp -r dist/* ../backend/static/

echo "=== Build complete ==="
