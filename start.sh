#!/bin/bash
set -e

echo "=== Support Knowledge Copilot ==="
echo "Starting ingestion pipeline..."

# Run ingestion to build the index
python ingest.py

echo "Starting Streamlit app..."

# Start Streamlit
streamlit run app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true