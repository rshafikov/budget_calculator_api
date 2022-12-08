FROM python:3.9-slim
RUN mkdir /app
COPY . /app
RUN pip3 install -r app/requirements.txt --no-cache-dir
WORKDIR /app
CMD ["python3", "main.py"]