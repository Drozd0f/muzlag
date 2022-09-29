FROM python:3 as base
WORKDIR /muzlag
RUN apt -y update && apt -y upgrade && apt install -y ffmpeg
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

FROM base as dev
RUN pip install jurigged
CMD jurigged -v main.py
