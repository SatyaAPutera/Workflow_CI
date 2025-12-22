FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY MLProject/ /app/MLProject/
COPY requirements.txt* /app/ 2>/dev/null || true

# Install Python dependencies
WORKDIR /app/MLProject
RUN pip install --no-cache-dir -r conda_requirements.txt || \
    pip install --no-cache-dir mlflow pandas scikit-learn numpy matplotlib scipy

# Create mlruns directory
RUN mkdir -p /app/mlruns

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MLFLOW_TRACKING_URI=/app/mlruns

# Default command
CMD ["python", "modelling.py"]
