# Task ID: T306, T326, T328
# Dockerfile for MCP server with optimizations
FROM python:3.13-slim

WORKDIR /app

# Create non-root user for security
RUN groupadd -g 1001 python && useradd -m -u 1001 -g python python

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    dumb-init \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies with pip
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=python:python . .

# Switch to non-root user
USER python

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]
# Start the application
CMD ["python", "mcp_server.py"]