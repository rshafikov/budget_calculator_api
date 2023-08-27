FROM python:3.9-slim
RUN mkdir /app
COPY . /app
RUN pip3 install -r app/requirements.txt --no-cache-dir
WORKDIR /app
#RUN python3 manage.py migrate
#RUN python3 manage.py load_categories