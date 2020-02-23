import telegram
from time import sleep
from PIL import Image
import requests
from io import BytesIO

chat_id = 143627371

# Telegram Bot Authorization Token
bot = telegram.Bot('1040937582:AAGQyo4u5aWU-Ahq6_xkkN4WtXY__bD40NY')


def sendPhoto(bot):
    print("Send photo")
    response = requests.get('http://0.0.0.0:5000/image.jpg')
    bot.send_photo(chat_id=chat_id, photo=BytesIO(response.content))
