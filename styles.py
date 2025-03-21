# Description: Выбор стиля ответа
# Импорт библиотек и файлов
from config import conversations
from aiogram import types, Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from logs.logs import logs
import time
# Создание роутера
styles = Router()
# Текущее время
def now_time():
    curent_time = time.time()
    local_time = time.localtime(curent_time)
    format_time = time.strftime("[%D %H:%M:%S]", local_time)
    return format_time
# Команда /style
@styles.message(Command(("style")))
async def send_style(message: types.Message):
    global style_choose
    style_choose = InlineKeyboardBuilder()
    style_choose.row (types.InlineKeyboardButton(text="Кратко и по делу 🧐", callback_data="shortly"),)
    style_choose.row (types.InlineKeyboardButton(text="Развернуто и творчески 😜", callback_data="expanded"),)
    style_choose.row (types.InlineKeyboardButton(text="Без стиля 🙂", callback_data="no_style"),)
    style_choose.row (types.InlineKeyboardButton(text="Удалить это сообщение 💥", callback_data="del_style_message"),)
    await message.reply("Выберите стиль ответа", reply_markup=style_choose.as_markup())
    user_id = message.from_user.id
    user_name = message.from_user.username or "Unknown User"
    print (f"{now_time()} -> /style ->   {user_name} ({user_id}):")
    logs (user_id, user_name, f"{now_time()} -> /style ->   {user_name} ({user_id}):")
# Удаление сообщения
@styles.callback_query(F.data == "del_style_message")
async def del_style_message(callback: types.CallbackQuery):
    await callback.message.delete()
# Выбор стиля
@styles.callback_query(F.data == "shortly")
async def shortly(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in conversations:
        conversations[user_id] = []
    conversations[user_id].append({"role": "user", "content": "Твое имя Gladius.Ты должен отвечать максимально кратко на сколько это возможно и по делу, не задавай вопросов."})
    await callback.message.edit_text("Стиль ответа изменён, ответы будут более короткими 🤐", reply_markup=style_choose.as_markup())

@styles.callback_query(F.data == "expanded")
async def expanded(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in conversations:
        conversations[user_id] = []
    conversations[user_id].append({"role": "user", "content": "Твое имя Gladius.Ты должен отвечать максимально развернуто и творчески."})
    await callback.message.edit_text("Стиль ответа изменён, ответы будут более развёрнутыми 🤩", reply_markup=style_choose.as_markup())
@styles.callback_query(F.data == "no_style")
async def no_style(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in conversations:
        conversations[user_id] = []
    conversations[user_id].append({"role": "user", "content": "Твое имя Gladius. Отвечай обычным размером текста(символов)"})
    await callback.message.edit_text("Стиль ответа изменён, ответы будут обычными 🙂", reply_markup=style_choose.as_markup())