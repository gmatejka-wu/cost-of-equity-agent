FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Smithery uses startCommand from smithery.yaml, so no ENTRYPOINT needed
