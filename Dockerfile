FROM python:3 as base
WORKDIR /muzlag
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y ffmpeg
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
