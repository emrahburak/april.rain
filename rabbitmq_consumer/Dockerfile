 FROM pypy:3.9-bullseye
# FROM python:3.9-alpine


WORKDIR /usr/src/app

COPY requirements.txt ./

RUN mkdir -p /var/watchdir
RUN mkdir -p /var/destination
RUN mkdir -p /var/chunk

RUN apt-get update && apt-get install -y ffmpeg 

RUN pip install --no-cache-dir -r requirements.txt

ENV CHUNK  '/var/chunk'

COPY . .

# EXPOSE 5000

 CMD [ "pypy", "./consumer.py" ]