# Dockerfile for Django Phone Book App

FROM python:3.12-slim
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Collect static files
RUN python3 manage.py collectstatic --noinput

CMD ["/bin/sh", "-c", "python3 manage.py migrate && gunicorn phone_book.phone_book.wsgi:application --bind 0.0.0.0:8080"]
