# Multi-stage build for audit-packages-tool
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN pip install --no-cache-dir build

# Copy source code
COPY . .

# Build the package
RUN python -m build

# Production stage
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r audituser && useradd -r -g audituser audituser

# Set working directory
WORKDIR /app

# Copy built package from builder stage
COPY --from=builder /app/dist/*.whl .

# Install the package
RUN pip install --no-cache-dir *.whl && rm *.whl

# Switch to non-root user
USER audituser

# Set entrypoint
ENTRYPOINT ["audit-packages"]

# Default command
CMD ["--help"]
