FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel

ENV PYENV_SHELL=/bin/bash

ENV GOOGLE_APPLICATION_CREDENTIALS=./secrets/data-service-account.json

WORKDIR /preprocess
COPY requirements.txt .

RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential git

RUN pip install -r requirements.txt

RUN mkdir -p /preprocess /secrets

ADD . /preprocess