# ============================================================================
# Multi-stage Dockerfile for Python Application
# ============================================================================
# Build: docker build -t myapp -f docker/Dockerfile .
# Run:   docker run -p 8000:8000 myapp

# ----------------------------------------------------------------------------
# Stage 1: Builder
# ----------------------------------------------------------------------------
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy and install the application
COPY pyproject.toml .
COPY src/ ./src/
RUN pip install .

# ----------------------------------------------------------------------------
# Stage 2: Production
# ----------------------------------------------------------------------------
FROM python:3.11-slim as production

# Labels
LABEL maintainer="your.email@example.com" \
    version="0.1.0" \
    description="MyApp - Sample Python Application"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production \
    PORT=8000

# Create non-root user
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY --chown=appuser:appgroup src/ ./src/

# Switch to non-root user
USER appuser

# Expose port
EXPOSE ${PORT}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:${PORT}/health').raise_for_status()" || exit 1

# Run the application
CMD ["sh", "-c", "uvicorn myapp.api:app --host 0.0.0.0 --port ${PORT}"]

# ----------------------------------------------------------------------------
# Stage 3: Development (optional)
# ----------------------------------------------------------------------------
FROM production as development

USER root

# Install development tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Install dev dependencies
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

# Copy all source files
COPY --chown=appuser:appgroup . .

USER appuser

# Enable reload for development
CMD ["sh", "-c", "uvicorn myapp.api:app --host 0.0.0.0 --port ${PORT} --reload"]
