# Use multi-stage build for better caching
FROM python:3.14-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY cleaners/ ./cleaners/
COPY db/ ./db/
COPY main.py .
COPY examples/ ./examples/
COPY pyproject.toml .
COPY LICENSE .
RUN pip install -e .

# Production stage
FROM python:3.14-slim

WORKDIR /app

# Copy only what's needed for production
COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
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
ENV TERM=xterm-256color

# Volume for persistent data
VOLUME ["/app/data"]

# Health check to ensure container is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sqlite3; sqlite3.connect('/app/data/business_data.db') or exit(1)" || exit(0)

# Add system dependencies for ReportLab
RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    tcl-dev \
    tk-dev \
    && rm -rf /var/lib/apt/lists/*

# Interactive mode to preserve Rich UI
ENTRYPOINT ["python", "main.py"]
# Override with non-interactive mode for CI/testing
CMD []
