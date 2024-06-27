# Use a Python 3.6 slim base image
FROM python:3.6-slim

# Set up directories
RUN mkdir /application
WORKDIR /application

# Install necessary packages for ROOT
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*
    
# Download and install ROOT
RUN wget https://root.cern/download/root_v6.24.06.Linux-ubuntu20-x86_64-gcc9.3.tar.gz && \
    tar -xzf root_v6.24.06.Linux-ubuntu20-x86_64-gcc9.3.tar.gz && \
    extracted_dir=$(tar -tf root_v6.24.06.Linux-ubuntu20-x86_64-gcc9.3.tar.gz | head -1 | cut -f1 -d"/") && \
    mv $extracted_dir /application/root && \
    rm root_v6.24.06.Linux-ubuntu20-x86_64-gcc9.3.tar.gz


# Set environment variables for ROOT
ENV ROOTSYS /application/root
ENV PATH $ROOTSYS/bin:$PATH
ENV LD_LIBRARY_PATH $ROOTSYS/lib:$LD_LIBRARY_PATH
ENV PYTHONPATH $ROOTSYS/lib:$PYTHONPATH

# Create a virtual environment
RUN python -m venv /venv

# Activate the virtual environment
ENV PATH="/venv/bin:$PATH"

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the application code
COPY . .

# Set permissions for the static folder
RUN chgrp -R 0 /application/static && \
    chmod -R g=u /application/static

# Environment variables
ENV PYTHONUNBUFFERED 1

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8001
STOPSIGNAL SIGINT

ENTRYPOINT ["python"]
CMD ["flask_app.py"]
