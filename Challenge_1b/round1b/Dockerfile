# Use full Debian-based image (NOT slim or alpine)
FROM python:3.10-bullseye

# Set working directory
WORKDIR /app

# Fix HTTP to HTTPS in APT sources and install system dependencies
RUN sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y \
    python3-pip python3 python3-dev \
    poppler-utils tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project
COPY . .

# Default command
CMD ["python", "run_collection.py"]
