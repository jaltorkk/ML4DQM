# Inherit python image
FROM python:3.6-slim

# Set up directories
RUN mkdir /application
WORKDIR /application

# Copy python dependencies and install these
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Copy the rest of the applicationssd
COPY . .
RUN chgrp -R 0 /application/static && \
    chmod -R g=u /application/static


# Environment variables
ENV PYTHONUNBUFFERED 1

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8001
STOPSIGNAL SIGINT

ENTRYPOINT ["python"]
CMD ["flask_app.py"]
