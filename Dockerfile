# Inherit python image
FROM python:3.9-slim-buster

# Set up directories
RUN mkdir /application
WORKDIR /application

# Copy python dependencies and install these
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /application/flask_session

# Copy the rest of the application
COPY . .

RUN chgrp -R 0 /application/static && \
    chmod -R g=u /application/static

RUN chgrp -R 0 /application/flask_session && \
    chmod -R g=u /application/flask_session

RUN chgrp -R 0 /tmp && \
    chmod -R g=u /tmp

# Environment variables
ENV PYTHONUNBUFFERED 1

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8001
STOPSIGNAL SIGINT

ENTRYPOINT ["python"]
CMD ["app.py"]


# Use a Python 3.6 slim base image
#FROM python:3.6-slim

# Set up directories
#RUN mkdir /application
#WORKDIR /application

# Set environment variables for ROOT
#ENV ROOTSYS /application/root
#ENV PATH $ROOTSYS/bin:$PATH
#ENV LD_LIBRARY_PATH $ROOTSYS/lib:$LD_LIBRARY_PATH
#ENV PYTHONPATH $ROOTSYS/lib:$PYTHONPATH

# Create a virtual environment
#RUN python -m venv /venv

# Activate the virtual environment
#ENV PATH="/venv/bin:$PATH"

# Copy the requirements file and install dependencies
#
COPY requirements.txt .
#RUN pip install --upgrade pip && \
#    pip install -r requirements.txt

# Copy the application code
#COPY . .

# Set permissions for the static folder
#RUN chgrp -R 0 /application/static && \
#    chmod -R g=u /application/static

# Environment variables
#ENV PYTHONUNBUFFERED 1

# EXPOSE port 8000 to allow communication to/from server
#EXPOSE 8001
#STOPSIGNAL SIGINT

#ENTRYPOINT ["python"]
#CMD ["flask_app.py"]
