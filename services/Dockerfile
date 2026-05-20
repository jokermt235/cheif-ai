FROM python:3.11

ENV PYTHONUNBUFFERED=1

RUN apt-get update \
  && apt-get install -y libpq-dev \
  && apt-get install -y libzbar-dev \
  && apt-get install -y apt-utils \
  && apt-get install -y gettext \
  && apt-get install -y python3-dev \
  && apt-get install -y libwebp-dev \
  && pip install --upgrade pip \
  && pip install "poetry>=1.6.1,<1.7.0" \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY services/pyproject.toml /app/
COPY services/. /app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
