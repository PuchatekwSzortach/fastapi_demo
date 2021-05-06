# syntax = docker/dockerfile:experimental

FROM python:3.10.0b1-slim-buster

# Install a few necessary need or useful libs and apps
RUN apt update && apt install -y wget vim

# # Install python environment
COPY ./requirements.txt /tmp/requirements.txt
RUN --mount=type=cache,mode=0777,target=/root/.cache/pip pip install -r /tmp/requirements.txt

# Setup bashrc
COPY ./docker/bashrc /root/.bashrc

# Setup PYTHONPATH
ENV PYTHONPATH=.

# # Set up working directory
WORKDIR /app
