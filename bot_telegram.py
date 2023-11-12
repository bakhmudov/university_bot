from create_bot import bot, dp
from aiogram.utils import executor
from database import sqllite_db
from handlers import admin_side, user_side


async def on_startup(_):
    sqllite_db.sql_start()
    print('Bot_online')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
