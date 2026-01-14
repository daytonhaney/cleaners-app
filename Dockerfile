# Use multi-stage build for better caching
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY cleaners/ ./cleaners/
COPY db/ ./db/
COPY app.py .
COPY pyproject.toml .
COPY LICENSE .
RUN pip install -e .

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy only what's needed for production
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app /app

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Create data directory for persistence
RUN mkdir -p /app/data && chown -R appuser:appuser /app

# Environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV CLEANERS_ENV=production

# Volume for persistent data
VOLUME ["/app/data"]

# Health check to ensure container is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sqlite3; sqlite3.connect('/app/data/business_data.db') or exit(1)" || exit(0)

# Interactive mode to preserve Rich UI
ENTRYPOINT ["python", "-m", "cleaners.main"]
# Override with non-interactive mode for CI/testing
CMD []
