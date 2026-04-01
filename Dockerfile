# ================ Builder Stage (install dependencies) ================
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

# Install build dependencies only in builder stage
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install packages (build wheels here)
RUN pip install --no-cache-dir -r requirements.txt

# ================ Runtime Stage (final small image) ================
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install only the runtime dependency for PostgreSQL client (much smaller than build tools)
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy your application code
COPY . .

EXPOSE 8000

# Run as non-root user
RUN useradd -m -u 1000 appuser
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]