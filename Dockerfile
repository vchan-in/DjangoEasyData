# Use Ubuntu 20.04 as the base image
FROM ubuntu:20.04

EXPOSE 8000

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3.8 python3.8-dev python3-pip \
        gcc automake default-libmysqlclient-dev pkg-config \
        netcat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure Python 3.8 is the default
RUN ln -sf /usr/bin/python3.8 /usr/bin/python

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Copy the wait-for-mysql script **before switching to a non-root user**
COPY wait-for-mysql.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/wait-for-mysql.sh

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Create non-root user and adjust permissions
RUN adduser --uid 5678 --disabled-password --gecos "" appuser && \
    chown -R appuser /app

# Switch to non-root user AFTER setting script permissions
USER appuser

CMD ["bash", "/usr/local/bin/entrypoint.sh"]
