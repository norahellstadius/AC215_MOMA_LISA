FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel

ENV PYENV_SHELL=/bin/bash

ENV GOOGLE_APPLICATION_CREDENTIALS=./secrets/data-service-account.json
ENV WANDB_API_KEY_PATH=./secrets/wandb_api_key.json

WORKDIR /train
COPY requirements.txt .

RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential git

RUN pip install -r requirements.txt

RUN mkdir -p /train /secrets

ADD . /train