import config
from aiogram import Bot, Dispatcher


bot = Bot(token=config.bot_token)
dp = Dispatcher(bot)
