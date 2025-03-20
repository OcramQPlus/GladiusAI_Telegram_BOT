import asyncio

from aiogram import types
from aiogram.enums import ParseMode

from config  import conversations, mistral_client
import prompts
import admin
import time


from logs.logs import logs
from forai import last_request_time, RATE_LIMIT, now_time, waiting_response_generator




async def mistral_answer(message: types.Message):
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
        logs (user_id, user_name, f"{now_time()} -> Сообщение пользователя -> {user_name} ({user_id}): {message.text}")
        

        
        waiting_response_generator_result = waiting_response_generator()
        waiting_msg = await message.reply(waiting_response_generator_result)
        print(f"{now_time()} -> Сообщение ожидания для ->   {user_name} ({user_id}):", waiting_response_generator_result)
        logs (user_id, user_name, f"{now_time()} -> Сообщение ожидания для -> {user_name} ({user_id}): {waiting_response_generator_result}")
        
        if user_id not in conversations:
            conversations[user_id] = []
        if not conversations[user_id]: 
            conversations[user_id] = [{"role": "system", "content": admin.default_prompts}]
            
        conversations[user_id].append({"role": "user", "content": message.text})
        
        if len(conversations[user_id]) > 1000:
            conversations[user_id] = [{"role": "system", "content": admin.default_prompts}] + conversations[user_id][-9:]
            
        response_text = ""
        
        for chunk in mistral_client.chat.stream(
            model=admin.mistral_model,
            messages=conversations[user_id],
        ):
            response_text += chunk.data.choices[0].delta.content or ""
        
        conversations[user_id].append({"role": "assistant", "content": response_text})
        print(f"{now_time()} -> Gladius message ->   {user_name} ({user_id}): {response_text}")
        print(f"{now_time()} -> Используемая языковая модель ->   {user_name} ({user_id}):", admin.mistral_model)
        logs (user_id, user_name, f"{now_time()} -> Gladius message -> {user_name} ({user_id}): {response_text}")
        logs (user_id, user_name, f"{now_time()} -> Используемая языковая модель -> {user_name} ({user_id}): {admin.mistral_model}")
        
        if admin.debug_mode == True:
            debug_model = f"\nМодель: {admin.mistral_model}"
            await waiting_msg.edit_text(response_text + debug_model)
        else:
            await waiting_msg.edit_text(response_text)
            
    except Exception as e:
        print(f"{now_time()} -> [Error]: {str(e)}")
        logs (user_id, user_name, f"{now_time()} -> [Error]: {str(e)}")
        await waiting_msg.edit_text(f"Произошла ошибка, обратитесь к разработчику(не обязательно): {str(e)} \nЕсли ошибка повторилась попробуйте /clear")
        
        
        
