import time 
import telegram.ext #pip install python-telegram-bot==13.13
import telegram
import subprocess
import requests
import re
import random
import os
import logging
import asyncio
from threading import Thread, Lock
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
from telegram import Update, ForceReply
from datetime import datetime


stat_command = '''echo $(uname -a | awk '{print $1, $2, $3, $13}' | tr ' ' '_') $(date "+%Y-%m-%d %H:%M:%S") CPU: $(top -b -n 1 | awk '/Cpu\(s\)/ {print 100 - $8"%"}') Temp:$(echo "scale=2; $(cat /sys/class/thermal/thermal_zone0/temp) / 1000" | bc) Up: $(uptime | awk '{print $3}' | sed 's/,//g')'''
network_command =  ''' echo $(ifconfig eth0) ; echo   $(ifconfig wlan0) ; echo $(iwconfig wlan0) '''

bot_token = os.environ.get("ENV_TLG_API_RASP_MON")
print(f"token={bot_token}")

telegram_notify = telegram.Bot(bot_token)

CHAT_ID = 0
CHAT_ID_PATH =  os.path.expanduser("/var/rasp-monitor/telegram_chat_id")

async def monitorPiTemp():
    global loop, CHAT_ID
    while True: 
        if CHAT_ID == 0:
            continue
        result = None
        network_result = None
        try:
            result = subprocess.check_output(stat_command, shell=True, text=True)
            logging.info(f"result={result}")
        except subprocess.CalledProcessError as e:
            logging.info(f"Error: {e}")
        logging.info(f"Chat ID: {CHAT_ID}")

        send_result = telegram_notify.send_message(chat_id=CHAT_ID, text=result)
        logging.info(f"send stat result = {send_result}")
        try:
            network_result = subprocess.check_output(network_command, shell=True, text=True)
            logging.info(f"result={network_result}")
        except subprocess.CalledProcessError as e:
            logging.info(f"Error: {e}")
        send_result = telegram_notify.send_message(chat_id=CHAT_ID, text=network_result)
        logging.info(f"send stat result = {send_result}")

        time.sleep(3600*6)

def monitorPiTempThread(loop):
    loop.run_until_complete(monitorPiTemp())

def get_chat_id(update, context):
    global CHAT_ID
    chat_id = update.message.chat_id
    CHAT_ID=chat_id
    with open(CHAT_ID_PATH, 'w') as file:
        file.write(str(chat_id))
    logging.info(f"Chat ID: {chat_id}")

def is_internet_available():
    try:
        subprocess.check_output(["ping", "-c", "1", "-W", "2", "8.8.8.8"])
        return True
    except subprocess.CalledProcessError:
        return False

def wait_for_internet():
    while not is_internet_available():
        logging.info("Internet not available. Waiting...")
        time.sleep(1)  # Wait for 5 seconds before checking again

    logging.info("Internet connection is available!")

def main():
    current_date=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=os.path.expanduser(f"/var/rasp-monitor/log_{current_date}.txt"))    
    global CHAT_ID

    try:
        with open(CHAT_ID_PATH, 'r') as file:
            CHAT_ID = int(file.read())
    except FileNotFoundError:
        CHAT_ID = 0

    if bot_token is not None:
        logging.info(f'Env is {bot_token}')
    else:
        logging.info(f'Env is not set!')
    
    # time.sleep(3600*6)

    wait_for_internet()

    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_chat_id))

    updater.start_polling()

    loop = asyncio.get_event_loop()

    thread1 = Thread(target = monitorPiTempThread,args=(loop,))
    thread1.start()

if __name__ == '__main__':
    main()

# sudo vi /etc/systemd/system/my_script.service
# docker run -it --rm --name=rasp-monitor  -v /home/pi/Rasp-Monitor/docker-folder/:/var/rasp-monitor	truongkutetk97/rasp-monitor:0.1  

'''
docker-compose up -d
docker exec -it rasp-monitor bash
docker build -t truongkutetk97/rasp-monitor:0.1 .

'''



'''
DockerFile
# FROM python:3
FROM ghcr.io/linuxserver/baseimage-ubuntu:arm64v8-jammy
USER root
RUN apt update 
RUN  apt install -y  python3 pip python-is-python3  
RUN pip install python-telegram-bot==13.13 
RUN pip install requests
RUN apt install -y net-tools wireless-tools  iputils-ping bc 
ADD monitor.py /
ENTRYPOINT ["python", "/monitor.py"]
# CMD ["bash"]
'''

'''
DockerCompose
version: '3'
services:
  rasp-monitor:
    image: truongkutetk97/rasp-monitor:0.1
    container_name: rasp-monitor-2
    user: root
    network_mode: host
    privileged: true  # Add this line to enable the --privileged flag
    environment:
      ENV_TLG_API_RASP_MON: ""
    volumes:
      - /home/pi/Rasp-Monitor/docker-folder/:/var/rasp-monitor
    restart: unless-stopped
'''