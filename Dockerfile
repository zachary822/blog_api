FROM python:3.10-slim

RUN apt update
RUN apt install -y curl

ENV POETRY_HOME="/root/.poetry"
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$PATH:$POETRY_HOME/bin:/usr/local/bin"
RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN  poetry install --no-root

COPY . .

ENV NEW_RELIC_CONFIG_FILE=newrelic.ini
CMD newrelic-admin run-program uvicorn api.main:app --port $PORT --host 0.0.0.0
