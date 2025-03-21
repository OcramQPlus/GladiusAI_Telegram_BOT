# Description: Получение ответа от MistralAI
# Импорт библиотек и файлов
import asyncio
from aiogram import types
from aiogram.enums import ParseMode
from config  import conversations, mistral_client
import admin
import time
from logs.logs import logs
from forai import last_request_time, RATE_LIMIT, now_time, waiting_response_generator
# Обработка сообщений от пользователя и отправка ответа
async def mistral_answer(message: types.Message):
    try:
        # Защита от спама
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
        # Получение конфигурации пользователя
        last_request_time[user_id] = current_time
        config = admin.get_user_config(message.from_user.id)
        user_name = message.from_user.username or "Unknown User"
        print(f"{now_time()} -> Сообщение пользователя ->   {user_name} ({user_id}): {message.text}")
        logs (user_id, user_name, f"{now_time()} -> Сообщение пользователя -> {user_name} ({user_id}): {message.text}")
        # Отправка и выбор сообщения ожидания
        waiting_response_generator_result = waiting_response_generator()
        waiting_msg = await message.reply(waiting_response_generator_result)
        print(f"{now_time()} -> Сообщение ожидания для ->   {user_name} ({user_id}):", waiting_response_generator_result)
        logs (user_id, user_name, f"{now_time()} -> Сообщение ожидания для -> {user_name} ({user_id}): {waiting_response_generator_result}")
        # Создание чата
        if user_id not in conversations:
            conversations[user_id] = []
        if not conversations[user_id]: 
            conversations[user_id] = [{"role": "system", "content": config["default_prompts"]}]
        conversations[user_id].append({"role": "user", "content": message.text})
        # Ограничение длины истории сообщений
        if len(conversations[user_id]) > 100:
            conversations[user_id] = [{"role": "system", "content": config["default_prompts"]}] + conversations[user_id][-9:]
        # Отправка сообщения и получение ответа
        response_text = ""
        for chunk in mistral_client.chat.stream(
            model=config["mistral_model"],
            messages=conversations[user_id],):
            response_text += chunk.data.choices[0].delta.content or ""
        # Запись ответа в историю сообщений
        conversations[user_id].append({"role": "assistant", "content": response_text})
        # Вывод ответа и модели
        print(f"{now_time()} -> Gladius message ->   {user_name} ({user_id}): {response_text}")
        print(f"{now_time()} -> Используемая языковая модель ->   {user_name} ({user_id}):", config["mistral_model"],)
        logs (user_id, user_name, f"{now_time()} -> Gladius message -> {user_name} ({user_id}): {response_text}")
        logs (user_id, user_name, f"{now_time()} -> Используемая языковая модель -> {user_name} ({user_id}): {config["mistral_model"],}")
        # Вывод ответа + проверка на debug_mode
        if config["debug_mode"] == True:
            debug_model = f"\nМодель: {config["mistral_model"],}"
            await waiting_msg.edit_text(response_text + debug_model)
        else:
            await waiting_msg.edit_text(response_text)
    # Обработка ошибок
    except Exception as e:
        print(f"{now_time()} -> [Error]: {str(e)}")
        logs (user_id, user_name, f"{now_time()} -> [Error]: {str(e)}")
        await waiting_msg.edit_text(f"Произошла ошибка, обратитесь к разработчику(не обязательно): {str(e)} \nЕсли ошибка повторилась попробуйте /clear")
        
        
        
