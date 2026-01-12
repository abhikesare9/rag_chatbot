
# Use official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY . .

# Upgrade pip and install dependencies
RUN pip install -r ./agent/requirements.txt

# Copy application code


# Expose port (if your agent runs as API)
EXPOSE 8000

# Run the agent (CHANGE this to your entry file)
CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8000"]
