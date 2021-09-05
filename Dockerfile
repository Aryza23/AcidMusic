# Python Based Docker
FROM debian:latest

RUN apt update && apt upgrade -y

#Installing Requirements
RUN apt install git curl python3-pip ffmpeg -y

#Installing Pytgcalls
RUN pip install py-tgcalls -U

#Fix Lib
RUN pip install matplotlib

#Fix Pyrogram 
RUN pip install git+https://github.com/pyrogram/pyrogram -U

#Updating Pip
RUN pip3 install -U pip
RUN pip install Pillow

COPY . /app
WORKDIR /app
RUN pip3 install -U -r requirements.txt
CMD python3 -m AcidMusic

