FROM python:3.9.16-buster

RUN apt-get -y update && apt-get -y upgrade \
    && apt-get install -y --no-install-recommends ffmpeg

COPY ./requirements.txt /requirements.txt
RUN pip install install -r requirements.txt
