import sqlite3
from sqlite3 import IntegrityError
from create_bot import bot
from datetime import datetime

base = sqlite3.connect('university_bot_db')
cursor = base.cursor()


def sql_start():
    if base:
        print('База данных подключена')
    cursor.execute('CREATE TABLE IF NOT EXISTS users (tg_id INTEGER, name_group TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS news (dt DATETIME, title VARCHAR(255), content TEXT, img TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS groups (name VARCHAR(6) PRIMARY KEY, schedule TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS questions (user_id INT, question TEXT, nick VARCHAR(50))')

    base.commit()


# methods for "SCHEDULE"
async def get_group(name):
    return [i for i in cursor.execute('SELECT * FROM groups WHERE name = ?', (name,))]


async def get_only_such_users(name):
    return [i for i in cursor.execute('SELECT * FROM users WHERE name_group = ?', (name,))]


async def create_schedule(state):
    data = await get_data_from_proxy(state)
    cursor.execute('UPDATE groups SET schedule = ? WHERE name = ?',
                   (data['image'], data['group']))
    base.commit()


async def delete_schedule(name):
    cursor.execute('UPDATE groups SET schedule = ? WHERE name = ?', (None, name))
    base.commit()


# methods for the "NEWS" table
async def get_data_from_proxy(state):
    async with state.proxy() as data:
        return data


async def add_news(state):
    proxy_data = await get_data_from_proxy(state)
    cursor.execute('INSERT INTO news VALUES (?, ?, ?, ?)', (datetime.now(),) + tuple(proxy_data.values()))
    base.commit()


async def get_news():
    return [_ for _ in cursor.execute('SELECT * FROM news')]


async def delete_news(date):
    datetime_obj = datetime.strptime(date, ' %Y-%m-%d %H:%M:%S.%f')
    cursor.execute('DELETE FROM news WHERE dt = ?', (datetime_obj,))
    base.commit()


# methods for the "GROUPS" table
async def get_all_groups():
    return [_ for _ in cursor.execute('SELECT * FROM groups')]


async def delete_group(name):
    cursor.execute('DELETE FROM groups WHERE name = ?', (name,))
    base.commit()


async def add_group(name, msg):
    try:
        cursor.execute('INSERT INTO groups VALUES (?, ?)', (name, None))
        base.commit()
    except IntegrityError:
        bot.send_message(msg.chat.id, 'Такая группа уже существует')


async def add_user(user_id):
    cursor.execute('INSERT INTO users VALUES (?, ?)', (user_id, 'no_group'))
    base.commit()


async def get_all_users():
    return [_ for _ in cursor.execute('SELECT * FROM users')]


async def change_user_group(user_id, group_name):
    cursor.execute('UPDATE users SET name_group = ? WHERE tg_id = ?', (group_name, user_id))
    base.commit()


# methods for the "QUESTIONS" table
async def delete_question(user_id):
    cursor.execute('DELETE FROM questions WHERE user_id = ?', (user_id,))
    base.commit()


def get_all_questions():
    return [_ for _ in cursor.execute('SELECT * FROM questions')]


async def add_question(state):
    data = await get_data_from_proxy(state)
    cursor.execute('INSERT INTO questions VALUES (?, ?, ?)', (data['user_id'],
                                                              data['question'],
                                                              data['nick'],))
    base.commit()


async def get_schedule_for_user(user_id):
    user_group = cursor.execute('SELECT name_group FROM users WHERE tg_id = ?',
                                (user_id,)).fetchone()
    if user_group:
        group_schedule = cursor.execute('SELECT schedule FROM groups WHERE name = ?',
                                        (user_group[0],)).fetchone()
        if group_schedule:
            return group_schedule[0]
    return None
