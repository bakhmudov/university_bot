from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware


storage = MemoryStorage()

bot = Bot(token='6968096217:AAGYhGiZLVIUFFXNT2OoXv-jI14VS1Kx5fM')
ADMINS_CHAT_ID = ''

dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
