# Use an official Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency specifications
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all repository contents into the container
COPY . .

# Set default entrypoint command to run the pipeline orchestrator
CMD ["python", "analysis/scripts/run_all.py"]
