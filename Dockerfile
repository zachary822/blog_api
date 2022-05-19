FROM python:3.10-slim

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --deploy --system

COPY . .

ENV NEW_RELIC_CONFIG_FILE=newrelic.ini
CMD newrelic-admin run-program uvicorn api.main:app --port $PORT --host 0.0.0.0
