FROM python:3.10-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /passage-app/
WORKDIR /passage-app/
COPY ./src/ /passage-app/
COPY ./requirements/base.txt /passage-app/base-req.txt 
COPY ./.env .env


RUN set -ex \
    && BUILD_DEPS=" \
        build-essential \
        libpcre3-dev \
        libpq-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && apt-get install -y --no-install-recommends default-libmysqlclient-dev \
    && pip install -U pip \
    && pip install --no-cache-dir -r /passage-app/base-req.txt 
