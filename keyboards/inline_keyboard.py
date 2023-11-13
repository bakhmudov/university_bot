from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_delete_news_keyboard(date):
    kb = InlineKeyboardMarkup()
    btn_delete = InlineKeyboardButton('Удалить новость', callback_data=f'news {date}')
    kb.add(btn_delete)
    return kb


async def create_reply_keyboard(user_id):
    kb = InlineKeyboardMarkup()
    reply = InlineKeyboardButton('Ответить', callback_data=f'qtn {user_id}')
    kb.add(reply)
    return kb
