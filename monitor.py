import logging
import telegram
import telegram.ext #pip install python-telegram-bot==13.13


import requests
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
import time 
from telegram import Update, ForceReply
from threading import Thread, Lock
import random
import subprocess
import re
import os
import asyncio

stat_command = '''echo $(uname -a | awk '{print $1, $2, $3, $13}' | tr ' ' '_') $(date "+%Y-%m-%d %H:%M:%S") CPU: $(top -b -n 1 | awk '/Cpu\(s\)/ {print 100 - $8"%"}') Temp:$(vcgencmd measure_temp | awk -F"=" '{print $2}') Up: $(uptime | awk '{print $3}' | sed 's/,//g')'''
network_command =  ''' echo $(ifconfig eth0) ; echo   $(ifconfig wlan0) ; echo $(iwconfig wlan0) '''

bot_token = os.environ.get("ENV_TLG_API_RASP_MON")
bot_user_name = "raspmonitor967_bot"

telegram_notify = telegram.Bot(bot_token)

CHAT_ID = 0
CHAT_ID_PATH =  os.path.expanduser("~/telegram_chat_id")

async def monitorPiTemp():
    global loop, CHAT_ID
    while True: 
        if CHAT_ID == 0:
            continue
        result = None
        network_result = None
        try:
            result = subprocess.check_output(stat_command, shell=True, text=True)
            print(f"result={result}")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
        print(f"Chat ID: {CHAT_ID}")

        telegram_notify.send_message(chat_id=CHAT_ID, text=result)

        try:
            network_result = subprocess.check_output(network_command, shell=True, text=True)
            print(f"result={network_result}")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
        telegram_notify.send_message(chat_id=CHAT_ID, text=network_result)

        # time.sleep(1)
        time.sleep(3600*6)

def monitorPiTempThread(loop):
    loop.run_until_complete(monitorPiTemp())


def get_chat_id(update, context):
    global CHAT_ID
    chat_id = update.message.chat_id
    CHAT_ID=chat_id
    with open(CHAT_ID_PATH, 'w') as file:
        file.write(str(chat_id))
    print(f"Chat ID: {chat_id}")

def main():
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')    
    global CHAT_ID

    try:
        with open(CHAT_ID_PATH, 'r') as file:
            CHAT_ID = int(file.read())
    except FileNotFoundError:
        CHAT_ID = 0

    if bot_token is not None:
        print(f'Env is {bot_token}')
    else:
        print(f'Env is not set!')


    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_chat_id))

    updater.start_polling()

    loop = asyncio.get_event_loop()

    thread1 = Thread(target = monitorPiTempThread,args=(loop,))
    thread1.start()

if __name__ == '__main__':
    main()