# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies including Node.js
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Upgrade pip and install dependencies
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# Copy package.json first for better Docker layer caching
COPY package.json /app/

# Install Node.js dependencies
RUN npm install

# Copy the rest of the application code
COPY . /app

# Build Tailwind CSS for production
RUN npm run build-css-prod

# Expose port 8000 to the outside world
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
