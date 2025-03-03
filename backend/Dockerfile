FROM python:3.13-alpine

LABEL org.opencontainers.image.authors="zacheryfudge+docker@gmail.com"

WORKDIR /backend
COPY . /backend/
RUN mkdir -p /var/logs/csg/

RUN apk add gcc python3-dev

RUN pip install -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/backend/src

ENV FLASK_APP=/backend/src/__init__.py
ENV FLASK_ENV=development

EXPOSE 5075

CMD ["flask", "run", "--port=5075", "--host=0.0.0.0", "--reload"]
