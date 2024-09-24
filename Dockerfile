# Use a Python 3.6 slim base image
FROM python:3.6-slim

# Install dependencies for Conda and ROOT
RUN apt-get update && apt-get install -y \
    wget \
    bzip2 \
    ca-certificates \
    libglib2.0-0 \
    libxext6 \
    libsm6 \
    libxrender1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

# Set environment variables for Conda
ENV PATH /opt/conda/bin:$PATH

# Update Conda
RUN conda update -n base -c defaults conda -y

# Create Conda environment and install Python 3.6 and ROOT
RUN conda create -n myenv python=3.6 root -c conda-forge -y

# Set up directories
RUN mkdir /application
WORKDIR /application

# Activate the Conda environment
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

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

# Expose port 8001 to allow communication to/from the server
EXPOSE 8001
STOPSIGNAL SIGINT

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "myenv", "python"]
CMD ["flask_app.py"]

