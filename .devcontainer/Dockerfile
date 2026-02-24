# Use official Python 3.12 image as base
FROM python:3.12-slim-bookworm

WORKDIR /workspaces/ai-transcript-app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    git \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv system-wide
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv \
    && mv /root/.local/bin/uvx /usr/local/bin/uvx \
    && chmod +x /usr/local/bin/uv /usr/local/bin/uvx

# Copy backend dependency files
COPY backend/pyproject.toml backend/uv.lock ./backend/
RUN cd backend && uv sync

# Verify
RUN python --version && uv --version