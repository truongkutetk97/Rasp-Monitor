# FROM python:3
FROM ubuntu:22.04
USER root
RUN apt update

RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt-cache search python3.1
RUN export TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt install -y  python3.12
RUN apt install -y pip
RUN apt install -y python-is-python3
RUN python --version

RUN pip install python-telegram-bot==13.13 
RUN pip install requests

RUN apt install -y net-tools wireless-tools  iputils-ping bc 

RUN pip install wakeonlan
RUN pip install scapy

ADD monitor.py /

ENTRYPOINT ["python", "/monitor.py"]
# CMD ["bash"]


