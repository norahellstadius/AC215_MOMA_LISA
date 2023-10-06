FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel

#ENV PYENV_SHELL=/bin/bash

ENV GOOGLE_APPLICATION_CREDENTIALS=./secrets/data-service-account.json

WORKDIR /train
COPY requirements.txt .

RUN pip install -r requirements.txt \
    mkdir -p /train && \
    mkdir -p /secrets

# Source code
ADD . /train
#
## Entry point
#ENTRYPOINT ["/bin/bash"]
#
## Get into the pipenv shell
#CMD ["-c", "pipenv shell"]