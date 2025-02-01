FROM python:3.8-alpine

LABEL org.opencontainers.image.authors="zacheryfudge+docker@gmail.com"

WORKDIR /uno
COPY . /uno/
RUN mkdir -p /var/logs/uno/

RUN apk add gcc python3-dev

RUN pip install -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/uno/
ENV FLASK_APP=backend

EXPOSE 5075
