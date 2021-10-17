import logging
import telegram
import telegram.ext
import requests
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import time 
from telegram import Update, ForceReply
from threading import Thread, Lock
import random
import subprocess
import re

bot_token = "dummy"
bot_user_name = "raspalarm_bot"
telegram_notify = telegram.Bot(bot_token)
monitor_status= 0
pattern_temp = 'temp=(.*)'
pattern_cpu = 'top.*up (.*),.*user.*load average: (.*)\n.*\n.*\n.*Mem :(.*).*total.*,(.*).*used'

def send_notify_message(telegram, chat_id, message):
    try:
        telegram.send_message(chat_id=chat_id, text=message,
                                parse_mode='Markdown')
    except Exception as ex:
        print(ex)

def monitorPiTemp():
    global monitor_status
    # logging.info("start monitor")
    while True: 
        # logging.info("Looping")
        result = subprocess.run([ "cat", "/thermal_zone0/temp"], stdout=subprocess.PIPE)
        # result = subprocess.run([ "cat", "/sys/class/thermal/thermal_zone0/temp"], stdout=subprocess.PIPE)
        # matchObj = re.match(pattern_temp,result.stdout.decode('utf-8') )
        # print(matchObj.group(1))
        # temp=matchObj.group(1)
        temp_str=result.stdout.decode('utf-8')
        print(type(temp_str))
        temp=round((int(temp_str))/1000,2)

        result2 = subprocess.run([ "top", "-bn1"], stdout=subprocess.PIPE)
        matchObj = re.match(pattern_cpu,result2.stdout.decode('utf-8') )
        print(matchObj.group(1))
        print(matchObj.group(2))
        print(matchObj.group(3).strip())
        print(matchObj.group(4).strip())
        uptime=matchObj.group(1)
        cpu=matchObj.group(2)
        totalmem=matchObj.group(3).strip()
        usedmem=matchObj.group(4).strip()

        status="Temp:{}, Uptime:{}, CPU:{}, Mem:{}/{}".format(temp,uptime,cpu,usedmem,totalmem)
        print(status)
        telegram_notify.send_message(chat_id="1156336235", text=status,
                                parse_mode='Markdown')
        time.sleep(60)
        if monitor_status ==0:
            break


def start_monitoring(update: Update, context: CallbackContext) -> None:
    global monitor_status
    monitor_status =1
    update.message.reply_text('Starting...')
    time.sleep(0.2)
    update.message.reply_text('.')
    time.sleep(0.2)
    update.message.reply_text('.')
    time.sleep(0.2)
    update.message.reply_text('.')
    time.sleep(0.2)
    update.message.reply_text('.')
    time.sleep(0.2)
    update.message.reply_text('.')
    time.sleep(0.2)
    update.message.reply_text('Started!')

    global monitoringThread
    monitoringThread = Thread(target = monitorPiTemp)
    monitoringThread.start()

def stop_monitoring(update: Update, context: CallbackContext) -> None:
    global monitor_status
    global monitoringThread
    monitor_status =0
    monitoringThread.join()
    update.message.reply_text('Stopping...')
    if not monitoringThread.is_alive():
        update.message.reply_text('Stopped!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Fucking idiot!')

def main():
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')    
    telegram_notify.send_message(chat_id="1156336235", text="RaspAlarm has up!",
                                parse_mode='Markdown')    

    updater = Updater(bot_token,use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("startmonitor", start_monitoring))
    dispatcher.add_handler(CommandHandler("stopmonitor", stop_monitoring))
    dispatcher.add_handler(CommandHandler("help", help_command))
    updater.start_polling()

    # while True:
    #     logging.info("TruongDepTrai")
    #     time.sleep(2)

if __name__ == '__main__':
    main()