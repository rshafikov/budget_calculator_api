FROM python:3.10-slim as python-base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

FROM python-base as prod
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN pip install --no-cache /usr/src/app/wheels/*