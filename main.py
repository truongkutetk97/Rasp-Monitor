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

#Config logging


bot_token = "dummy"
bot_user_name = "raspalarm_bot"
URL = "the heroku app link that we will create later"
MY_USER_ID = "1156336235"
global bot
global TOKEN
TOKEN = bot_token
telegram_notify = telegram.Bot(TOKEN)
potentialCoin = ["BTC", "ETH", "ADA", "BNB", "XRP", "SOL", "DOT"]
monitor_status = 0

def monitorPiTemp():
    global monitor_status
    logging.info("start monitor")
    while True:
        dirrection = random.randint(1,2)
        income = round(random.uniform(0.0000,50.0000),4)
        coin = random.choice(potentialCoin)
        delay =random.randint(10,20)
        print("Next message in ... {}".format(delay))
        logging.info("Nextmessage in {} monitorstatus {}".format(delay, monitor_status))
        if dirrection == 1:
            msg = "Balance change: {} +{}$".format(coin, income)
            send_notify_message(telegram= telegram_notify, chat_id = "1156336235", message = msg)
        elif dirrection == 2:
            msg = "Balance change: {} -{}$".format(coin, income)
            send_notify_message(telegram= telegram_notify, chat_id = "1156336235", message = msg)
        time.sleep(delay)
        if monitor_status ==0:
            break

monitoringThread = Thread(target = monitorPiTemp)

def start_monitoring(update: Update, context: CallbackContext) -> None:
    global monitor_status
    global monitoringThread
    """Send a message when the command /startmonitor is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi TruongDepTrai, I have just enabled the monitoring for you\!',
    )
    monitor_status =1
    if not monitoringThread.is_alive():
        monitoringThread = Thread(target = monitorPiTemp)
    monitoringThread.start()

def stop_monitoring(update: Update, context: CallbackContext) -> None:
    global monitor_status
    global monitoringThread
    """Send a message when the command /stopmonitor is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi TruongDepTrai, I have just disabled the monitoring for you\!',
    )
    monitor_status =0
    monitoringThread.join()

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Fucking idiot!')

def send_notify_message(telegram, chat_id, message):
    try:
        telegram.send_message(chat_id=chat_id, text=message,
                                parse_mode='Markdown')
    except Exception as ex:
        print(ex)

def monitorPiTemp():
    while True:
        dirrection = random.randint(1,2)
        income = round(random.uniform(0.0000,50.0000),4)
        coin = random.choice(potentialCoin)
        if dirrection == 1:
            msg = "Balance change: {} +{}$".format(coin, income)
            send_notify_message(telegram= telegram_notify, chat_id = "1156336235", message = msg)
        elif dirrection == 2:
            msg = "Balance change: {} -{}$".format(coin, income)
            send_notify_message(telegram= telegram_notify, chat_id = "1156336235", message = msg)
        time.sleep(5)

def main():
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')    
    logging.info("HIIiiiiiiiii")
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("startmonitor", start_monitoring))
    dispatcher.add_handler(CommandHandler("stopmonitor", stop_monitoring))
    dispatcher.add_handler(CommandHandler("help", help_command))
    send_notify_message(telegram= telegram_notify, chat_id = "1156336235", message = "RaspAlarm Bot online")
    updater.start_polling()
    # updater.idle()

    while True:
        logging.info("TruongDepTrai")
        send_notify_message(telegram= telegram_notify, chat_id = "1156336235", message = "TruongDepTrai")
        time.sleep(5)

if __name__ == '__main__':
    main()
    input()
