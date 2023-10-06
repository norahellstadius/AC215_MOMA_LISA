FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel

ENV PYENV_SHELL=/bin/bash

ENV WANDB_API_KEY=./secrets/wandb_api_key.json.json

WORKDIR /train
COPY requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir -p /train /secrets

ADD . /train