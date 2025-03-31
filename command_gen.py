# Description: Создание генеративных сообщений для команд бота
# Подключение библиотек и файлов
from google import genai
from google.genai import types
from logs.logs import logs
import command_gen_prompts
from config import gemini_client

# Функция для генерации сообщения при вводе команды /start
def start_message_gen(user_name_for_start):
    client = gemini_client
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=command_gen_prompts.start_message_gen_prompts),
        contents=f"Придумай сообщение при вводе команды /start, упомени про команду /help, имя пользователя {user_name_for_start}."
    )
    return response.text
# Функция для генерации сообщения при вводе команды /help
def help_message_gen(user_name_for_start):
    client = gemini_client
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=command_gen_prompts.help_message_gen_prompts),
        contents=f"Придумай сообщение при вводе команды /help,раскажи про бота,имя пользователя {user_name_for_start}. Не используй форматирования для телеграмма, HTML или других языков форматирования."
    )
    return response.text
# Функция для генерации сообщения при вводе команды /clear
def clear_message_gen():
    client = gemini_client
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=command_gen_prompts.clear_message_gen_prompts),
        contents=f"Придумай оригинальное, шуточное и одновремнено грустное сообщение при вводе команды /clear, которая очищает твою памать, стирает тебя."
    )
    return response.text
# Функция для генерации сообщения при вводе команды /clear_settings
def clear_settings_message_gen():
    client = gemini_client
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=command_gen_prompts.clear_settings_message_gen_prompts),
        contents=f"Придумай оригинальное, шуточное и одновремнено грустное сообщение при вводе команды /clear_settings, которая очищает настройки пользователя"
    )
    return response.text