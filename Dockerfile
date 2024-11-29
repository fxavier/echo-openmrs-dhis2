FROM python:3.9-alpine3.13
LABEL maintainer="xavierfrancisco353@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt


WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache \
    #  nodejs \
    #  npm \
      postgresql-client \
      gcc \
      libc-dev \
      make \
      git \
      libffi-dev \
      openssl-dev \
      python3-dev \
      libxml2-dev \
      libxslt-dev \
      build-base \
      postgresql-dev \
      musl-dev \
      linux-headers && \
    /py/bin/pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home app && \
    # Clearing APK cache
    rm -rf /var/cache/apk/*

# Setting up application directories
RUN mkdir -p /vol/web/static /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol/web && \
    chmod -R 777 /py/*


COPY ./app /app


WORKDIR /app

EXPOSE 8000

ENV PATH="/py/bin:$PATH"

USER app