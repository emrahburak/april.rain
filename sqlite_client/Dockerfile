 FROM pypy:3.9-bullseye
# FROM python:3.9-alpine


WORKDIR /usr/src/app

COPY requirements.txt ./

RUN mkdir -p /var/data

# RUN apt-get update && apt-get install -y ffmpeg 

RUN pip install --no-cache-dir -r requirements.txt


COPY . .

# EXPOSE 5000

 CMD [ "pypy", "./main.py" ]