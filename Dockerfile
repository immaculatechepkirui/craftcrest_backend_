# Use official Python 3.10 slim image as base
FROM python:3.10-slim

# Install system build dependencies needed for your packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libdbus-1-dev \
    libcups2-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Copy your requirements.txt first for Docker layer caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the app code
COPY . .

# Specify the command to run your app (adjust as needed)
CMD ["python", "app.py"]
