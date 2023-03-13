# Build: docker build -t pgrab:latest .
# Run: docker run -it --rm pgrab -h

# Base Image
FROM python:3.11-alpine

# Maintainer
LABEL maintainer="Shivam Saraswat <thecybersapien@protonmail.com>"
LABEL description="PGrab is a banner grabber tool used to gather information about a remote server or device, specifically the banner or header information that is sent when a connection is made."

# Install OS Dependencies
RUN apk update && apk upgrade && apk add --no-cache bash gcc libffi-dev musl-dev curl

# Set Work Directory
WORKDIR /usr/src/app
# Copy Project
COPY . .

# setup virtualenv
RUN python3 -m venv venv
RUN . venv/bin/activate

# Install Project Dependencies
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

# Start with console arguments passed to docker run
ENTRYPOINT ["python3", "main.py"]