FROM python:3.10-slim

# Prevent Python buffering
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (PDF support)
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose Hugging Face port
EXPOSE 7860

# Run FastAPI
CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "7860"]
