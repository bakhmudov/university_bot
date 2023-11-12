from create_bot import bot
from database import sqllite_db


async def sending_schedule(name):
    users = await sqllite_db.get_only_such_users(name)
    group = await sqllite_db.get_group(name)

    for user in users:
        await bot.send_photo(user[0], group[0][1], caption='РАСПИСАНИЕ ВАШЕЙ ГРУППЫ ОБНОВЛЕНО')
