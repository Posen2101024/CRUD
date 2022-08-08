FROM ubuntu:20.04

ARG TZ="Asia/Taipei"
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Advanced Packaging Tools
ARG DEBIAN_FRONTEND="noninteractive"
RUN apt-get update \
 && apt-get upgrade -y \
    build-essential \
    curl \
    python3.8 \
    python3.8-dev \
    python3-distutils \
    tzdata \
    vim \
 && rm -rf /var/lib/apt/lists/*

# Python3.8
WORKDIR /tmp
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
 && python3.8 get-pip.py \
 && rm get-pip.py
RUN ln -s /usr/bin/python3.8 /usr/local/bin/python
RUN ln -s /usr/bin/python3.8 /usr/local/bin/python3

# Entrypoint
WORKDIR /usr/local/bin
COPY entrypoint.sh .
ENTRYPOINT ["entrypoint.sh"]

# Django
WORKDIR /crud
COPY crud .
ENV DJANGO_SETTINGS_MODULE="crud.settings"
ENV PYTHONPATH="$PYTHONPATH:/crud"
RUN pip install --no-cache-dir --upgrade --requirement requirements.txt
