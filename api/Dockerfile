FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies with scikit-learn version pinned to match model
RUN pip install --no-cache-dir scikit-learn==1.3.0 && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY api/ ./api/
COPY model/ ./model/
COPY data/ ./data/

# Environment variables
ENV DATA_PATH=./data/creditcard.csv
ENV MODEL_PATH=./model/saved_models/model.pkl
ENV PORT=8000
ENV AUTH_USERNAME=admin
ENV AUTH_PASSWORD=password

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/metrics')" || exit 1

# Run the application
CMD ["python", "api/app.py"]