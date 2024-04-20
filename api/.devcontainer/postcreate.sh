#!/usr/bin/bash

sudo chown -R ${USER}:${USER} ${HOME} \
  && sudo  pip3 install -U --no-cache-dir pip \
  && sudo pip3 install -U --no-cache-dir uv \
  && uv venv ${VIRTUAL_ENV} \
  && uv pip install --no-cache -U pip \
  && uv pip install --no-cache  -r .devcontainer/requirements.txt \
  && uv pip install --no-cache -U  pydot packaging setuptools black bandit