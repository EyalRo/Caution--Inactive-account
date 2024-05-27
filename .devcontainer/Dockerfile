FROM python:slim
EXPOSE 8000

ARG DEBIAN_FRONTEND=noninteractive

### Install git ###
RUN apt update
RUN apt install --quiet --yes git 

### Copy code to container ###
RUN mkdir -p /usr/src/app
COPY . /usr/src/app
WORKDIR /usr/src/app

### Run pip for python reqs
RUN pip install --quiet -r requirements.txt

### 🐟 Fish shell! 🐟 
SHELL ["fish", "--command"]

RUN chsh -s /usr/bin/fish

ENV SHELL /usr/bin/fish
ENV LANG=C.UTF-8 LANGUAGE=C.UTF-8 LC_ALL=C.UTF-8

ENTRYPOINT [ "fish" ]