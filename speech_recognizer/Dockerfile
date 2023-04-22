FROM python:3.9.16-bullseye
# FROM pypy:3.9-bullseye
# FROM python:3.9-alpine


WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt-get update && apt-get install -y ffmpeg 

RUN pip install --no-cache-dir -r requirements.txt


COPY . .

# EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
# CMD [ "python", "./consumer.py" ]