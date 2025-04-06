# Description: Получение отзыва от пользователя
# Импорт библиотек и файлов
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types, F, Router
from aiogram.filters.command import Command
from forai import now_time
from logs.logs import logs 
import os
import time
import asyncio
from aiogram.enums import ParseMode
from forai import last_request_time
from aiogram.filters import BaseFilter
from aiogram.types import Message
import command_gen
import config
import forai
# Создание роутера
feedback_router = Router()
# Создание переменных
feedback_get = {}
RATE_LIMIT = 5
feedback_status = False
# Фильтр для проверки достуна
class Access_to_the_bot(BaseFilter):
    def __init__(self, user_access: list[int]):
        self.user_access = user_access
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.user_access
# Получение текущего времени
def now_time():
    curent_time = time.time()
    local_time = time.localtime(curent_time)
    format_time = time.strftime("[%D %H:%M:%S]", local_time)
    return format_time
# Создание функции для записи отзыва
def feedback(feedback_type, user_id, user_name, feedback_message):
    feedback_dir = "feedbacks"
    os.makedirs(feedback_dir, exist_ok=True) 
    feedback_path = os.path.join(feedback_dir, f"{feedback_type}.{user_id}.{user_name}.feedback")
    with open(feedback_path, "a", encoding="utf-8") as feedback_file:
        user_data = f"{user_name} ({user_id}):"
        feedback_file.write(f"{user_data} {feedback_message = }\n")
# Обработчика команды /feedback
@feedback_router.message(Access_to_the_bot(config.user_access_list),Command(("feedback")))
async def feedback_message(message: types.Message):
    user_name_for_start = message.from_user.username or ""
    user_id = message.from_user.id
    user_name = message.from_user.username or "Unknown User"
    feedback_menu = InlineKeyboardBuilder()
    feedback_menu.row (types.InlineKeyboardButton(text="Положительный 👍", callback_data="good_feedback"),)
    feedback_menu.row (types.InlineKeyboardButton(text="Отрицательный 👎", callback_data="bad_feedback"),)
    feedback_menu.row (types.InlineKeyboardButton(text="Идея 💡", callback_data="idea_feedback"),)
    await message.reply(f"{command_gen.feedback_start_message_gen(user_name_for_start,user_id,user_name)}", reply_markup=feedback_menu.as_markup())
    print(f"{now_time()} -> /feedback ->   {message.from_user.username} ({message.from_user.id}):")
    logs (message.from_user.id, message.from_user.username, f"{now_time()} -> /feedback -> {message.from_user.username} ({message.from_user.id}):")
    
# У пользователя нет доступа к боту
@feedback_router.message(Command(("feedback")))
async def feedback_message(message: types.Message):
    
    await message.reply(command_gen.user_access_list_gen(message.from_user.first_name,message.from_user.id, message.from_user.username))
    print(f"{forai.now_time()} -> Пользователь не получил доступа к боту->   {message.from_user.username} ({message.from_user.id}): {message.text}")
    logs(message.from_user.id, message.from_user.username, f"{forai.now_time()} -> Пользователь не получил доступа к боту-> {message.from_user.username} ({message.from_user.id}): {message.text}")
# Обработчики кнопок
@feedback_router.callback_query(F.data == "good_feedback")
async def good_feedback(callback: types.CallbackQuery):
    await callback.message.answer("Введите ваш положительный отзыв👍:")
    feedback_get[callback.from_user.id] = "good_feedback"
    global feedback_status
    feedback_status = True
@feedback_router.callback_query(F.data == "bad_feedback")
async def bad_feedback(callback: types.CallbackQuery):
    await callback.message.answer("Введите ваш отрицательный отзыв👎:")
    feedback_get[callback.from_user.id] = "bad_feedback"
    global feedback_status
    feedback_status = True
@feedback_router.callback_query(F.data == "idea_feedback")
async def idea_feedback(callback: types.CallbackQuery):
    await callback.message.answer("Введите вашу идею💡:")
    feedback_get[callback.from_user.id] = "idea_feedback"
    global feedback_status
    feedback_status = True
# Обработчик сообщения
async def feedback_message_write(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username or "Unknown User"
    current_time = time.time()
    try:
        # Защита от спама
        if user_id in last_request_time:
            time_passed = current_time - last_request_time[user_id]
            if time_passed < RATE_LIMIT:
                remaining = round(RATE_LIMIT - time_passed, 1)
                msg = await message.reply(f"""Попробуйте оставить отзыв позже
Через: {round(remaining)} сек. ⏳ """)
                await asyncio.sleep(RATE_LIMIT)
                await msg.edit_text("<b>Попробуйте ещё раз🎭</b>", parse_mode=ParseMode.HTML)
                return
        last_request_time[user_id] = current_time
    # Обработка ошибок
    except Exception as e:
        print(f"An error occurred: {e}")
        logs(user_id,user_name, f"An error occurred: {e}")
    # Получение отзыва
    user_name = message.from_user.username or "Unknown User"
    user_name_for_start = message.from_user.username or ""
    print(f"{now_time()} -> Отзыв пользователя ->   {user_name} ({user_id}): {message.text}")
    logs(user_id, user_name, f"{now_time()} -> Отзыв пользователя -> {user_name} ({user_id}): {message.text}")
    feedback_type = feedback_get[user_id]
    feedback_message = message.text
    feedback(feedback_type, user_id, user_name, f"{now_time()} -> {feedback_type} -> {feedback_message}")
    await message.reply(f"{command_gen.feedback_end_message_gen(user_name_for_start, feedback_type, feedback_message, user_id,user_name)}")
    del feedback_get[user_id]