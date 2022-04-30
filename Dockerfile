FROM python:3.9-slim

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --deploy --system

COPY . .

CMD uvicorn api.main:app --port $PORT --host 0.0.0.0
