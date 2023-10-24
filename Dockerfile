# FROM python:3
FROM ubuntu:23.04
USER root
RUN apt update

RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y  python3.12
RUN apt install -y pip
RUN apt install -y python-is-python3

RUN pip install python-telegram-bot==13.13 
RUN pip install requests

RUN apt install -y net-tools wireless-tools  iputils-ping bc 
ADD monitor.py /

ENTRYPOINT ["python", "/monitor.py"]
# CMD ["bash"]


