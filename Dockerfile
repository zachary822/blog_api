FROM python:3.11-slim as base

RUN apt update
RUN apt install -y curl libxml2-dev libxslt-dev python3-dev zlib1g-dev build-essential

ENV POETRY_HOME="/root/.poetry" \
    VENV_PATH="/app/.venv"
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$VENV_PATH/bin:$POETRY_HOME/bin:/usr/local/bin:$PATH"
RUN poetry config virtualenvs.create false

WORKDIR /app
RUN python -m venv $VENV_PATH
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

FROM python:3.11-slim
ENV VENV_PATH="/app/.venv"
RUN apt update && \
    apt install -y libxslt-dev
WORKDIR /app
COPY --from=base $VENV_PATH $VENV_PATH

COPY . .

ENV NEW_RELIC_CONFIG_FILE=newrelic.ini \
    PATH="$VENV_PATH/bin:$PATH"
CMD newrelic-admin run-program uvicorn api.main:app --port $PORT --host 0.0.0.0
