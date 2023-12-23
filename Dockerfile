FROM python:3.10.12-slim

RUN apt-get update \
    && apt-get install --no-install-recommends --yes \
    curl \
    gnupg2 \
    libffi-dev \
    libpq-dev

ARG PIP_VERSION=23.1.2
RUN pip install "pip==${PIP_VERSION}"

ARG POETRY_VERSION=1.5.0
RUN pip install "poetry==${POETRY_VERSION}"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev

RUN chmod +x ./server-entrypoint.sh
RUN chmod +x ./worker-entrypoint.sh