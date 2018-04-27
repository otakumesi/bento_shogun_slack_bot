FROM python:3.6

ADD . /tmp/bot

WORKDIR /tmp/bot

RUN pip install -r requirements.txt
