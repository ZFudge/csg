FROM python:3.13-alpine

LABEL org.opencontainers.image.authors="zacheryfudge+docker@gmail.com"

WORKDIR /backend
COPY . /backend/
RUN mkdir -p /var/logs/backend/

RUN apk add gcc python3-dev

RUN pip install -r requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:backend"
ENV FLASK_APP=/backend/app.py
ENV FLASK_ENV=development

EXPOSE 5075

CMD ["gunicorn", "--worker-class", "eventlet", "--workers", "1", "--bind", "0.0.0.0:5075", "-m", "007", "wsgi:app"]
