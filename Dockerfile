FROM python:3
# RUN apt update 
# RUN  apt install -y python3 pip python-is-python3  

ADD monitor.py /
RUN pip install python-telegram-bot requests 
VOLUME /thermal_zone0 
# RUN apt install -y libraspberrypi-bin
CMD [ "python3", "./monitor.py" ]

