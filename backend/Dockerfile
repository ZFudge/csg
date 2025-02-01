FROM python:3.8-alpine

LABEL org.opencontainers.image.authors="zacheryfudge+docker@gmail.com"

WORKDIR /uno
COPY . /uno/
RUN mkdir -p /var/logs/uno/

RUN apk add gcc python3-dev

RUN pip install -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/uno/
ENV FLASK_APP=/uno

EXPOSE 5075

CMD ["flask", "run", "--port=5075", "--host=0.0.0.0"]
