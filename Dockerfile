FROM python:3.8-alpine


RUN mkdir /app
WORKDIR /app


RUN apk add --no-cache gcc musl-dev zlib-dev jpeg-dev

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn mysql-connector-python

RUN apk del gcc musl-dev zlib-dev
