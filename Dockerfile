FROM python:3.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1

COPY ./poetry.lock /usr/src/app/
COPY ./pyproject.toml /usr/src/app

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . /usr/src/app
