FROM python:3.9.8

ADD requirements.txt /

RUN pip install --upgrade pip && pip install -r requirements.txt