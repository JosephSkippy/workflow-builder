FROM python:3.13-slim

WORKDIR /app

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files first (layer caching)
COPY pyproject.toml .
RUN uv sync --no-dev --no-install-project

# Copy application code
COPY app/ app/

# Copy seed data
COPY data/toronto.csv data/toronto.csv

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
