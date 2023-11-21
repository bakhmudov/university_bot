from aiogram import types


def group_keyboard(group_list):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for i in range(0, len(group_list), 3):
        row_buttons = group_list[i:i + 3]
        kb.row(*[types.KeyboardButton(group[0]) for group in row_buttons])
    return kb
