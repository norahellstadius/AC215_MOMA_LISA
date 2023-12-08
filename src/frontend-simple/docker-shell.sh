#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
# Automatic export to the environment of subsequently executed commands
# source: the command 'help export' run in Terminal
export IMAGE_NAME="frontend-simple"
export BASE_DIR=$(pwd)

# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .


# --v: Attach a filesystem volume to the container
# -p: Publish a container's port(s) to the host (host_port: container_port) (source: https://dockerlabs.collabnix.com/intermediate/networking/ExposingContainerPort.html)
# docker run --rm --name $IMAGE_NAME -it \
# -v "$BASE_DIR":/app \
# -p 8080:8080 $IMAGE_NAME \
# --network momalisa-app $IMAGE_NAME

docker run --rm --name $IMAGE_NAME -it \
-v "$BASE_DIR":/app \
-p 3000:3000 \
--network=momalisa-app $IMAGE_NAME