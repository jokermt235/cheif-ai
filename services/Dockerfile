FROM python:3

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get install -y libpq-dev \
  && apt-get install -y libzbar-dev \
  && apt-get install -y apt-utils \
  && apt-get install -y gettext \
  && apt-get install -y python3-dev \
  && apt-get install -y libwebp-dev

# Updating pip to latest version
RUN pip install --upgrade pip

RUN pip install "poetry>=1.6.1,<1.7.0"

WORKDIR /app
COPY services/pyproject.toml /app/

COPY services/. /app/

RUN echo "The files listed in app are"

RUN ls /app/

# Requirements are installed here to ensure they will be cached.
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
