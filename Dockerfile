FROM python:3.10-alpine

COPY requirements.txt /temp/requirements.txt
COPY . /src
WORKDIR /src

EXPOSE 8000

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password django-user

USER django-user
