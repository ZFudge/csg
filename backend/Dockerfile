FROM python:3.8-alpine

LABEL org.opencontainers.image.authors="zacheryfudge+docker@gmail.com"

WORKDIR /csg
COPY . /csg/
RUN mkdir -p /var/logs/csg/

RUN apk add gcc python3-dev

RUN pip install -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/csg/
ENV FLASK_APP=/csg
ENV FLASK_ENV=development

EXPOSE 5075

CMD ["flask", "run", "--port=5075", "--host=0.0.0.0", "--reload"]
