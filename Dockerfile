FROM python:3.11

RUN mkdir /app

COPY /kvartirnik_bot /app/kvartirnik_bot
COPY pyproject.toml /app

WORKDIR /app
ENV PYTHONPATH=/app

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
