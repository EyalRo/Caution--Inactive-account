FROM python:3.9.19-alpine3.20
EXPOSE 8000

RUN mkdir -p /usr/src/app
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install --upgrade pip
RUN pip3 install --user -r requirements.txt

