
import asyncio
import time

from google.genai import types as genai_types
from logs.logs import logs
from aiogram import types, Router
from aiogram.enums import ParseMode
from forai import last_request_time, RATE_LIMIT, now_time, waiting_response_generator
from config import conversations, gemini_client
import admin
import prompts
gemini = Router()



async def gemini_answer(message: types.Message):
    try:
        user_id = message.from_user.id
        current_time = time.time()
        if user_id in last_request_time:
            time_passed = current_time - last_request_time[user_id]
            if time_passed < RATE_LIMIT:
                remaining = round(RATE_LIMIT - time_passed, 1)
                msg = await message.reply(f"Повторите запрос через {round(remaining)} сек. ⏳. ")
                await asyncio.sleep(RATE_LIMIT)
                await msg.edit_text("<b>Повторите запрос 🎭</b>", parse_mode=ParseMode.HTML)
                await asyncio.sleep(3)
                await msg.delete()
                return
        last_request_time[user_id] = current_time
        user_name = message.from_user.username or "Unknown User"
        print(f"{now_time()} -> Сообщение пользователя ->   {user_name} ({user_id}): {message.text}")
        logs(user_id, user_name, f"{now_time()} -> Сообщение пользователя -> {user_name} ({user_id}): {message.text}")
        waiting_response_generator_result = waiting_response_generator()
        waiting_msg = await message.reply(waiting_response_generator_result)
        print(f"{now_time()} -> Сообщение ожидания для ->   {user_name} ({user_id}):", waiting_response_generator_result)
        logs(user_id, user_name, f"{now_time()} -> Сообщение ожидания для -> {user_name} ({user_id}): {waiting_response_generator_result}")
        
        if user_id not in conversations:
            conversations[user_id] = gemini_client.chats.create(model=admin.gemini_model, 
            config = genai_types.GenerateContentConfig(system_instruction= admin.default_prompts) )
        elif isinstance(conversations[user_id], list):
            conversations[user_id] = gemini_client.chats.create(model=admin.gemini_model , 
            config = genai_types.GenerateContentConfig(system_instruction= admin.default_prompts))
        
        response = conversations[user_id].send_message(message.text)
        response_text = response.text

        await waiting_msg.edit_text(response_text)
        
        print(f"{now_time()} -> Gladius message ->   {user_name} ({user_id}): {response_text}")
        print(f"{now_time()} -> Используемая языковая модель ->   {user_name} ({user_id}):", admin.gemini_model)
        logs(user_id, user_name, f"{now_time()} -> Gladius message -> {user_name} ({user_id}): {response_text}")
        logs(user_id, user_name, f"{now_time()} -> Используемая языковая модель -> {user_name} ({user_id}): {admin.gemini_model}")
        
    except Exception as e:
        print(f"{now_time()} -> [Error]: {str(e)}")
        logs(user_id, user_name, f"{now_time()} -> [Error]: {str(e)}")
        await waiting_msg.edit_text(f"Произошла ошибка, обратитесь к разработчику(не обязательно): {str(e)} \nЕсли ошибка повторилась попробуйте /clear")
# ...existing code...