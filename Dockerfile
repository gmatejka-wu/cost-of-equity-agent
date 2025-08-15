FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY main.py .

# Create a non-root user for security
RUN groupadd -r mcp && useradd -r -g mcp -d /app -s /bin/bash mcp && \
    chown -R mcp:mcp /app

USER mcp

# The command will be specified by Smithery based on smithery.yaml
