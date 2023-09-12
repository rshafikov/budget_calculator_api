FROM python:3.9-slim
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt --no-cache-dir
#RUN apt update -y && apt install dnsutils -y && nslookup db
#RUN python3 manage.py migrate && python3 manage.py load_categories
CMD ["gunicorn", "plus_balance.wsgi:application", "--bind", "0.0.0.0:8000"]