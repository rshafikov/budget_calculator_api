FROM python:3.9-slim
RUN mkdir /app
COPY . /app
RUN pip3 install -r app/requirements.txt --no-cache-dir
WORKDIR /app
CMD ["gunicorn", "plus_balance.wsgi:application", "--bind", "0.0.0.0:8000"]