# Inherit python image
FROM python:3.9-slim-buster

# Set up directories
RUN mkdir /application
WORKDIR /application

# Copy python dependencies and install these
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /applications
WORKDIR /applications

# Copy the rest of the application
COPY . .

# Set permissions for the static folder
RUN chgrp -R 0 /applications/static && \
    chmod -R g=u /applications/static

# Environment variables
ENV PYTHONUNBUFFERED 1

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8001
STOPSIGNAL SIGINT

ENTRYPOINT ["python"]
CMD ["flask_app.py"]

# Copy the requirements file and install dependencies
COPY requirements.txt .

