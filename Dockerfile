# Multi-stage Dockerfile for Smart Home Intent Classification

# Stage 1: Builder
FROM python:3.9 as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements_app.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --user -r requirements_app.txt

# Stage 2: Runtime
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/home/appuser/.local/bin:$PATH \
    PYTHONPATH=/app

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/data /app/models /app/docs && \
    chown -R appuser:appuser /app

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Pre-download Hugging Face model to avoid rate limits at runtime
ENV HF_HOME=/app/model_cache
RUN mkdir -p ${HF_HOME} && chown -R appuser:appuser ${HF_HOME}

# Copy source code
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser docs/ ./docs/
COPY --chown=appuser:appuser dataset.csv ./data/dataset.csv

# Switch to non-root user
USER appuser

# Trigger model download
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command: Run the Streamlit app
EXPOSE 8080
CMD ["sh", "-c", "streamlit run src/app.py --server.port=${PORT:-8080} --server.address=0.0.0.0"]
