FROM python:3
WORKDIR /muzlag
RUN apt -y update && apt -y upgrade && apt install -y ffmpeg
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
