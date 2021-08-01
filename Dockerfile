# syntax = docker/dockerfile:1.2
FROM python:3.9-slim-buster

# Set environment variables
ENV APP_HOME=/code
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
# See: https://github.com/Docker-Hub-frolvlad/docker-alpine-python3/pull/13
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR $APP_HOME

# Install dependencies & update
RUN apt-get update -y && apt-get install -y \
    --no-install-recommends netcat-openbsd gcc libpq-dev python3-dev libffi-dev curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./requirements $APP_HOME/requirements
RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip pip install -r requirements/development.txt

COPY . $APP_HOME

EXPOSE $PORT
