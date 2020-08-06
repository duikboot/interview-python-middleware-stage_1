FROM python:3.8.1 as builder

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8000
# CMD tail -f /dev/null
CMD gunicorn api.app:app -b 0.0.0.0:8000 --reload --log-level debug --access-logfile=- -t 9999
