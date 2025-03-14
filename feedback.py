
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types, F, Router
from aiogram.filters.command import Command

from forai import now_time
from logs.logs import logs 

import os
import time

import asyncio
from aiogram.enums import ParseMode

import mistralaibot

from forai import last_request_time



feedback_router = Router()
feedback_status = False
RATE_LIMIT = 30

def now_time():
    curent_time = time.time()
    local_time = time.localtime(curent_time)
    format_time = time.strftime("[%D %H:%M:%S]", local_time)
    return format_time

def feedback(feedback_type, user_id, user_name, feedback_message):
    feedback_dir = "feedbacks"
    os.makedirs(feedback_dir, exist_ok=True) 
    feedback_path = os.path.join(feedback_dir, f"{feedback_type}.{user_id}.{user_name}.feedback")
    with open(feedback_path, "a", encoding="utf-8") as feedback_file:
        user_data = f"{user_name} ({user_id}):"
        feedback_file.write(f"{user_data} {feedback_message = }\n")

        
        
@feedback_router.message(Command(("feedback")))
async def feedback_message(message: types.Message):
    feedback_menu = InlineKeyboardBuilder()
    feedback_menu.row (types.InlineKeyboardButton(text="Положительный 👍", callback_data="good_feedback"),)
    feedback_menu.row (types.InlineKeyboardButton(text="Отрицательный 👎", callback_data="bad_feedback"),)
    feedback_menu.row (types.InlineKeyboardButton(text="Идея 💡", callback_data="idea_feedback"),)
    await message.reply("Введите ваш отзыв🤗:", reply_markup=feedback_menu.as_markup())
    print(f"{now_time()} -> /feedback ->   {message.from_user.username} ({message.from_user.id}):")
    logs (message.from_user.id, message.from_user.username, f"{now_time()} -> /feedback -> {message.from_user.username} ({message.from_user.id}):")

    
@feedback_router.callback_query(F.data == "good_feedback")
async def good_feedback(callback: types.CallbackQuery):
    global feedback_type_user
    global feedback_status
    
    await callback.message.answer("Введите ваш положительный отзыв👍:")
    feedback_type_user = "good_feedback"
    feedback_status = True
    
@feedback_router.callback_query(F.data == "bad_feedback")
async def bad_feedback(callback: types.CallbackQuery):
    global feedback_type_user
    global feedback_status
    
    await callback.message.answer("Введите ваш отрицательный отзыв👎:")
    feedback_type_user = "bad_feedback"
    feedback_status = True

    
@feedback_router.callback_query(F.data == "idea_feedback")
async def idea_feedback(callback: types.CallbackQuery):
    global feedback_type_user
    global feedback_status
    
    await callback.message.answer("Введите вашу идею💡:")
    feedback_type_user = "idea_feedback"
    feedback_status = True
    
    

@feedback_router.message()
async def process_message(message: types.Message):
    global feedback_status
    if feedback_status == True:
        try:
            user_id = message.from_user.id
            current_time = time.time()
            if user_id in last_request_time:
                time_passed = current_time - last_request_time[user_id]
                feedback_status = False
                if time_passed < RATE_LIMIT:
                    remaining = round(RATE_LIMIT - time_passed, 1)
                    msg = await message.reply(f"""Попробуйте отсавть отзыв позже
Через: {round(remaining)} сек. ⏳ """)
                    await asyncio.sleep(RATE_LIMIT)
                    await msg.edit_text("<b>Попробуйте ещё раз🎭</b>", parse_mode=ParseMode.HTML)
                    return
            last_request_time[user_id] = current_time
        except Exception as e:
            print(f"An error occurred: {e}")
        user_id = message.from_user.id
        user_name = message.from_user.username or "Unknown User"
        print(f"{now_time()} -> Сообщение пользователя ->   {user_name} ({user_id}): {message.text}")
        logs (user_id, user_name, f"{now_time()} -> Сообщение пользователя -> {user_name} ({user_id}): {message.text}")
        feedback_type = feedback_type_user
        feedback_message = message.text
        feedback(feedback_type, user_id, user_name, f"{now_time()} -> {feedback_type} -> {feedback_message}")
        await message.reply("Спасибо за ваш отзыв!🤗")
        feedback_status = False
    else:
        await mistralaibot.process_message(message)
