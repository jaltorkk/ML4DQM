# Use a Python 3.6 slim base image
FROM python:3.6-slim

# Set up directories
RUN mkdir /application
WORKDIR /application

apt-get install binutils cmake dpkg-dev g++ gcc libssl-dev git libx11-dev \
libxext-dev libxft-dev libxpm-dev python3 libtbb-dev

#dnf install root
#dnf install root python3-root root-notebook

# Install necessary packages for ROOT
#RUN apt-get update && apt-get install -y \
#    wget \
#    curl \
#    git \
#    && rm -rf /var/lib/apt/lists/*
    
# Download and install ROOT
#RUN wget https://root.cern/download/root_v6.24.06.Linux-ubuntu20-x86_64-gcc9.3.tar.gz && \
#    mkdir /temp_root && \
#    tar -xzf root_v6.24.06.Linux-ubuntu20-x86_64-gcc9.3.tar.gz -C /temp_root && \
#    mv /temp_root/* /application/root && \
#    rm -rf /temp_root && \
#    rm root_v6.24.06.Linux-ubuntu20-x86_64-gcc9.3.tar.gz

# Install necessary packages for building ROOT
#RUN apt-get update && apt-get install -y \
#    wget \
#    curl \
#    git \
#    build-essential \
#    cmake \
#    python3-dev \
#    g++ \
#    gcc \
#    binutils \
#    libx11-dev \
#    libxpm-dev \
#    libxft-dev \
#    libxext-dev \
#    libssl-dev \
 #   libpcre3-dev \
 #   xlibmesa-glu-dev \
 #   libglew-dev \
 #   libftgl-dev \
 #   default-libmysqlclient-dev \
 #   libfftw3-dev \
 #   libcfitsio-dev \
#    graphviz \
#    libavahi-compat-libdnssd-dev \
 #   libldap2-dev \
 #   python-dev \
 #   libxml2-dev \
 #   libkrb5-dev \
 #   libgsl0-dev \
 #   qtbase5-dev \
 #   && rm -rf /var/lib/apt/lists/*

# Download and build ROOT from source
#RUN wget https://root.cern/download/root_v6.24.06.source.tar.gz && \
#    tar -xzf root_v6.24.06.source.tar.gz && \
#    mkdir root_build && cd root_build && \
#    cmake ../root-6.24.06 -DPYTHON3_EXECUTABLE=/usr/bin/python3.6 -Dpython3=ON && \
#    make -j$(nproc) && \
#    make install && \
#    rm -rf /root_build root_v6.24.06.source.tar.gz

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
