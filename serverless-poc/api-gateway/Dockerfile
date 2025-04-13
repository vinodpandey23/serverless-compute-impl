# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /api-gateway

# Set PYTHONPATH to include the app directory
ENV PYTHONPATH=/api-gateway

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code into container
COPY app /api-gateway

# Command to run the FastAPI app with Uvicorn [For docker compose]
CMD ["uvicorn", "api_gateway:app", "--host", "api-gateway", "--port", "8000"]