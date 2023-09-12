FROM python:3.9-slim as python-base
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

FROM python-base as prod
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN pip install --no-cache /usr/src/app/wheels/*