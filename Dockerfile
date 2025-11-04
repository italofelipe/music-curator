# ------------------------------------------------------------
# music_curator — FastAPI runtime (Python 3.14)
# Multi-stage build with Poetry for reproducible installs
# ------------------------------------------------------------

# --- Base image with build toolchain
FROM python:3.14-slim AS base

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# Install system deps required to compile common wheels (psycopg etc.)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        libpq-dev \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for better security
ARG APP_USER=app
ARG APP_UID=10001
RUN useradd -m -u ${APP_UID} -s /bin/bash ${APP_USER}

# Setup a dedicated virtualenv path
ENV VENV_PATH=/opt/venv
RUN python -m venv ${VENV_PATH}
ENV PATH="${VENV_PATH}/bin:$PATH"

# Install Poetry (no virtualenv creation inside Poetry — we manage it)
ENV POETRY_VERSION=1.8.3 \
    POETRY_HOME=/opt/poetry \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false
RUN curl -sSL https://install.python-poetry.org | python - \
    && ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

WORKDIR /app

# Copy only dependency manifests first for better layer caching
COPY pyproject.toml poetry.lock* /app/

# --- Build deps in a dedicated layer (including dev if specified)
FROM base AS builder

# Allow choosing whether to install dev dependencies at build time
ARG INSTALL_DEV=false

# Install deps into the venv deterministically via export -> pip
RUN ${VENV_PATH}/bin/pip install --upgrade pip setuptools wheel && \
    poetry lock --no-update && \
    if [ "$INSTALL_DEV" = "true" ]; then \
      poetry export -f requirements.txt --with dev --without-hashes -o /tmp/requirements.txt; \
    else \
      poetry export -f requirements.txt --only main --without-hashes -o /tmp/requirements.txt; \
    fi && \
    ${VENV_PATH}/bin/pip install -r /tmp/requirements.txt

# --- Final runtime image (smallest possible)
FROM python:3.14-slim AS runtime
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    VENV_PATH=/opt/venv

# Minimal runtime libs (libpq for psycopg)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq5 \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy virtualenv from builder
COPY --from=builder ${VENV_PATH} ${VENV_PATH}
ENV PATH="${VENV_PATH}/bin:$PATH"

# Create non-root user and working dir
ARG APP_USER=app
ARG APP_UID=10001
RUN useradd -m -u ${APP_UID} -s /bin/bash ${APP_USER}
WORKDIR /app

# Copy installed site-packages from builder (already in /opt/venv)
# Copy application code (kept last for better caching during dev)
COPY --chown=${APP_USER}:${APP_USER} ./src /app/src
COPY --chown=${APP_USER}:${APP_USER} ./alembic /app/alembic
COPY --chown=${APP_USER}:${APP_USER} ./alembic/alembic.ini /app/alembic.ini
COPY --chown=${APP_USER}:${APP_USER} pyproject.toml /app/pyproject.toml

# Runtime environment variables
ENV PORT=8000 \
    APP_ENV=production \
    PYTHONPATH=/app/src

USER ${APP_USER}

# Expose FastAPI default port
EXPOSE 8000

# Healthcheck: attempts to hit the /health endpoint
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s CMD python -c "import sys,urllib.request; \
    sys.exit(0) if urllib.request.urlopen('http://127.0.0.1:8000/health').getcode()==200 else sys.exit(1)" || exit 1

# Default command runs the API with uvicorn
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
