# Use Python 3.10 slim — matches your development environment
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first — Docker caches this layer
# If requirements don't change, this layer isn't rebuilt
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run ingestion first, then start Streamlit
# The shell script handles both steps
CMD ["bash", "start.sh"]