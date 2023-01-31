import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher


bot = Bot(token=os.getenv("BLOODRAVEN707BOTTOKEN"))
dp = Dispatcher(bot)
