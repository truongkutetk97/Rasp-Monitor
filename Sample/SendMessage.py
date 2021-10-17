import logging
import telegram
import telegram.ext
import requests
import re
from telegram.ext import Updater, CommandHandler
import time 

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

bot_token = "dummy"
bot_user_name = "truonglele_bot"
URL = "the heroku app link that we will create later"
MY_USER_ID = "1156336235"
global bot
global TOKEN
TOKEN = bot_token

# https://api.telegram.org/bot[TOKEN]/sendMessage?chat_id=[CHAT_ID]&text=[MY_MESSAGE_TEXT]


def send_notify_message(telegram, chat_id, message):
    try:
        telegram.send_message(chat_id=chat_id, text=message,
                                parse_mode='Markdown')
    except Exception as ex:
        print(ex)


def main():
    telegram_notify = telegram.Bot(TOKEN)
    while True:
        send_notify_message(telegram= telegram_notify, chat_id = "1156336235", message = "TruongDepTrai")
        time.sleep(5)

if __name__ == '__main__':
    main()