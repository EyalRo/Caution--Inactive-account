FROM python:slim

RUN mkdir -p /usr/src/app
COPY . /usr/src/app
WORKDIR /usr/src/app

ENTRYPOINT ["python3"]