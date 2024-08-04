FROM python:3.12 AS python-base

LABEL authors="rshafikov"

WORKDIR /app
COPY requirements* .
RUN pip install -U pip && pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


FROM python:3.12 AS prod

ENV PYTHONUNBUFFERED 1

COPY --from=python-base /usr/src/app/wheels /usr/src/app/wheels
RUN pip install --no-cache /usr/src/app/wheels/*
COPY . .


FROM python:3.12 AS test

ENV PYTHONUNBUFFERED 1

COPY --from=python-base /usr/src/app/wheels /usr/src/app/wheels
RUN pip install -U pip && pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements_test.txt
RUN pip install --no-cache /usr/src/app/wheels/*
COPY . .
