FROM python:3.13-slim

# Set the working directory
WORKDIR /workspacex

# Switch to root user to install packages
USER root

# Install required packages
RUN apt-get update && \
    apt-get install -y \
    redis-server \
    git \
    git-lfs \
    sudo \
    curl \
    cmake \
    build-essential \
    ca-certificates \
    debian-archive-keyring \
    libuuid1 \
    libtinfo6 \
    libssl3 \
    libsqlite3-0 \
    libreadline8 \
    libncursesw6 \
    liblzma5 \
    libgdbm6 \
    libffi8 \
    libdb5.3 \
    libc6 \
    libbz2-1.0 \
    tzdata \
    pkg-config \
    netbase && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set root password (not recommended for production)
RUN echo 'root:1234567' | chpasswd

# Create non-root user and set password
RUN useradd -m vscode && \
    echo 'vscode:123456' | chpasswd && \
    adduser vscode sudo

# Switch to the non-root user
USER vscode

# Copy requirements and install Python packages
COPY requirement.txt .
RUN pip install -r requirement.txt

# Expose the application port
EXPOSE 8000

# Copy the application code
COPY . /workspacex

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]