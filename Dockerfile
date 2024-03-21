FROM python:3.11-alpine

# Install build tools
RUN apk update && \
    apk add --no-cache gcc g++ musl-dev

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Set the command to run the application
CMD ["python", "app.py"]
