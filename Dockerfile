# FROM python:3
FROM ubuntu:23.04
USER root
RUN apt update
RUN  apt install -y  python3 pip python-is-python3  

RUN pip install python-telegram-bot==13.13 
RUN pip install requests

RUN apt install -y net-tools wireless-tools  iputils-ping bc 
ADD monitor.py /

ENTRYPOINT ["python", "/monitor.py"]
# CMD ["bash"]


