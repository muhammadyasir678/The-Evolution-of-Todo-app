# Multi-stage build for Redpanda
# This Dockerfile is for building a custom Redpanda image if needed
# For most cases, you'll use the official Redpanda image directly

FROM docker.redpanda.com/redpandadata/redpanda:v23.2.15

# Set working directory
WORKDIR /app

# Copy any custom configuration files if needed
# COPY redpanda.yaml /etc/redpanda/redpanda.yaml

# Expose ports
EXPOSE 9092 9093 8081 8082

# Default command to start Redpanda
CMD ["redpanda", "start", "--smp", "1", "--memory", "1G", "--reserve-memory", "100M", \
     "--overprovisioned", "--node-id", "0", "--check=false", \
     "--kafka-addr", "PLAINTEXT://0.0.0.0:9092,OUTSIDE://0.0.0.0:9093", \
     "--advertise-kafka-addr", "PLAINTEXT://localhost:9092,OUTSIDE://localhost:9093"]