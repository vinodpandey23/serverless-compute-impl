# Use official Python image
FROM python:3.11-slim

# Install Docker CLI
RUN apt-get update && apt-get install -y docker.io

# Set working directory
WORKDIR /function-manager

# Set PYTHONPATH to include the app directory
ENV PYTHONPATH=/function-manager

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code into container
COPY app /function-manager

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "function_manager:app", "--host", "function-manager", "--port", "5000"]