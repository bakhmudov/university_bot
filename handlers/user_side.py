from aiogram import types
from aiogram.dispatcher import FSMContext

from create_bot import bot, dp
from database import sqllite_db
from keyboards import usually_keyboard
from handlers import states
from handlers.admin_side import add_proxy_data


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    all_users_id = [id_[0] for id_ in await sqllite_db.get_all_users()]
    if message.from_user.id not in all_users_id:
        await sqllite_db.add_user(message.from_user.id)

    await bot.send_message(message.chat.id, 'Бот с расписанием ДГТУ. Помощь по командам напишите /help')
    await bot.send_message(message.chat.id, 'Выбери группу в которой учишься, либо напиши любой текст чтобы пропустить',
                           reply_markup=usually_keyboard.group_keyboard(await sqllite_db.get_all_groups()))
    await states.StartStates.group_name.set()


@dp.message_handler(state=states.StartStates.group_name)
async def start_state(message: types.Message, state: FSMContext):
    all_group_names = [_[0] for _ in await sqllite_db.get_all_groups()]
    if message.text in all_group_names:
        await sqllite_db.change_user_group(message.from_user.id, message.text)
        await bot.send_message(message.chat.id, f'Прикрепил тебя к группе {message.text}',
                               reply_markup=types.ReplyKeyboardRemove())
    else:
        await bot.send_message(message.chat.id, 'Ты пропустил выбор группы, но всегда сможешь'
                                                ' выбрать ее с помощью команды /select_group',
                               reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(commands=['select_group'])
async def select_group_command(message: types.Message):
    all_groups = await sqllite_db.get_all_groups()
    group_kb = usually_keyboard.group_keyboard(all_groups)
    await message.reply('Выбери группу', reply=False, reply_markup=group_kb)
    await states.SelectGroupStates.group_name.set()


@dp.message_handler(state=states.SelectGroupStates.group_name)
async def select_group_state(message: types.Message, state: FSMContext):
    all_group_names = [_[0] for _ in await sqllite_db.get_all_groups()]
    if message.text in all_group_names:
        await sqllite_db.change_user_group(message.from_user.id, message.text)
        await bot.send_message(message.chat.id, f'Группа изменена',
                               reply_markup=types.ReplyKeyboardRemove())
    else:
        await bot.send_message(message.chat.id, 'Группа, которую ты выбрал, не существует',
                               reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(commands=['delete_me_from_group'])
async def delete_from_group(message: types.Message):
    await sqllite_db.change_user_group(message.from_user.id, None)
    await message.reply('Группа успешно отвязана', reply=False)


@dp.message_handler(commands=['news', 'Новости'])
async def news_command(message: types.Message):
    news = await sqllite_db.get_news()
    for i in news[:3]:
        await bot.send_photo(message.chat.id, i[3], f'*{i[1]}*\n\n{i[2]}',
                             parse_mode='Markdown')


# // QUESTIONS //
@dp.message_handler(commands=['ask_question'])
async def ask_question_command(message: types.Message):
    await message.reply('Напишите свой вопрос', reply=False)
    await states.AskQuestionStates.get_question.set()


@dp.message_handler(state=states.AskQuestionStates.get_question)
async def get_question_state(message: types.Message, state: FSMContext):
    await add_proxy_data(state, {
        'user_id': message.from_user.id,
        'question': message.text,
        'nick': message.from_user.username,
    })
    await sqllite_db.add_question(state)
    await message.reply('Вопрос задана, ждите ответа...', reply=False)


@dp.message_handler(commands=['id'])
async def get_group_id(message: types.Message, state: FSMContext):
    await message.reply(message.chat.id)


@dp.message_handler(commands=['get_schedule'])
async def get_schedule_command(message: types.Message):
    user_id = message.from_user.id
    schedule = await sqllite_db.get_schedule_for_user(user_id)

    if schedule:
        await bot.send_message(message.chat.id, f'Ваше расписание:\n{schedule}')
    else:
        await bot.send_message(message.chat.id, 'Ваше расписание не найдено')
