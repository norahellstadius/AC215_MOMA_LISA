FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /workflow

# Copy only the dependencies file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


# # Start the application
# ENTRYPOINT [ "/bin/sh" ] 