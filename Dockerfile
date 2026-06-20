# Build stage: install dependencies into a clean layer
FROM python:3.12-slim AS builder

WORKDIR /app
COPY pyproject.toml .
# src/ must be present: pyproject's setuptools `packages.find where=["src"]`
# reads it while building the wheel, so copy it before installing.
COPY src/ ./src/
# Install only runtime deps (no dev extras like pytest/ruff)
RUN pip install --no-cache-dir --prefix=/install .

# Runtime stage: copy only what's needed — keeps the final image small
FROM python:3.12-slim

# Run as non-root — a container running as root is a security risk
RUN useradd --no-create-home --shell /bin/false appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY src/ ./src/

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
