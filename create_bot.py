import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher

# Для запуска через bot.bat
# bot = Bot( token = os.getenv('BLOODRAVEN707BOTTOKEN') )

# Для запуска без bot.bat
bot = Bot( token = 'токен_нужно_прописать_сюда' )
dp = Dispatcher( bot )
