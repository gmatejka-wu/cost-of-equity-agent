FROM python:3.11-slim

# Faster, quieter installs with sensible timeouts
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=100

# Only bring what's needed to build wheels; remove afterwards
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./

# Build wheels first (faster + deterministic in CI) then install from local dir
RUN pip wheel --wheel-dir=/wheels -r requirements.txt \
 && pip install --no-index --find-links=/wheels -r requirements.txt

# Copy the rest (keeps earlier layers cacheable)
COPY . .

# Smithery uses startCommand from smithery.yaml, so no ENTRYPOINT needed
