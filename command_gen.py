# Description: Создание генеративных сообщений для команд бота
# Подключение библиотек и файлов
from google.genai import types
from logs.logs import logs
import command_gen_prompts
from config import gemini_client
import time
import plugins


def now_time():
    curent_time = time.time()
    local_time = time.localtime(curent_time)
    format_time = time.strftime("[%D %H:%M:%S]", local_time)
    return format_time
# Функция для генерации сообщения при вводе команды /start
def start_message_gen(user_name_for_start, user_id, user_name):
    client = gemini_client
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=command_gen_prompts.start_message_gen_prompts),
        contents=f"Придумай сообщение при вводе команды /start, упомени про команду /help, имя пользователя {user_name_for_start}."
    )
    print(f"{now_time()} -> Сообщение ИИ для->   {user_name} ({user_id}): {response.text}")
    logs(user_id, user_name, f"{now_time()} -> Сообщение ИИ для-> {user_name} ({user_id}): {response.text}")
    return response.text
# Функция для генерации сообщения при вводе команды /help
def help_message_gen(user_name_for_start, user_id, user_name):
    client = gemini_client
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=command_gen_prompts.help_message_gen_prompts),
        contents=f"Придумай сообщение при вводе команды /help,раскажи про бота,имя пользователя {user_name_for_start}. Не используй форматирования для телеграмма, HTML или других языков форматирования."
    )
    print(f"{now_time()} -> Сообщение ИИ для->   {user_name} ({user_id}): {response.text}")
    logs(user_id, user_name, f"{now_time()} -> Сообщение ИИ для-> {user_name} ({user_id}): {response.text}")
    return response.text
# Функция для генерации сообщения при вводе команды /clear
def clear_message_gen(user_id, user_name):
    client = gemini_client
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=command_gen_prompts.clear_message_gen_prompts),
        contents=f"Придумай оригинальное, шуточное и одновремнено грустное небольшое сообщение при вводе команды /clear, которая очищает твою памать, стирает тебя."
    )
    user_name = user_name
    user_id = user_id
    print(f"{now_time()} -> Сообщение ИИ для->   {user_name} ({user_id}): {response.text}")
    logs(user_id, user_name, f"{now_time()} -> Сообщение ИИ для-> {user_name} ({user_id}): {response.text}")
    return response.text
# Функция для генерации сообщения при вводе команды /clear_settings
def clear_settings_message_gen(user_id, user_name):
    client = gemini_client
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=command_gen_prompts.clear_settings_message_gen_prompts),
        contents=f"Придумай оригинальное, шуточное и одновремнено грустное небольшое сообщение при вводе команды /clear_settings, которая очищает настройки пользователя"
    )
    user_name = user_name
    user_id = user_id
    print(f"{now_time()} -> Сообщение ИИ для->   {user_name} ({user_id}): {response.text}")
    logs(user_id, user_name, f"{now_time()} -> Сообщение ИИ для-> {user_name} ({user_id}): {response.text}")
    return response.text
# Функция для генерации сообщения при вводе команды /feedback
def feedback_start_message_gen(user_name_for_start, user_id, user_name):
    client = gemini_client
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=command_gen_prompts.feedback_message_gen_prompts),
        contents=f"Придмай оригинальное сообщения для того чтобы пользователя отправивиший команду /feedback, отставил хороший отзыв или идею, его имя{user_name_for_start}."
    )
    print(f"{now_time()} -> Сообщение ИИ для->   {user_name} ({user_id}): {response.text}")
    logs(user_id, user_name, f"{now_time()} -> Сообщение ИИ для-> {user_name} ({user_id}): {response.text}")
    return response.text
# Функция для генерации сообщения при вводе команды /feedback
def feedback_end_message_gen(user_name_for_start,feedback_type,feedback_message,user_id,user_name):
    client = gemini_client
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=command_gen_prompts.feedback_message_gen_prompts),
        contents=f"Придумай сообщение, в благодарность оставленного отзыва, тип отзыва{feedback_type}, имя пользователя{user_name_for_start}, сообщение пользователя {feedback_message}.")
    print(f"{now_time()} -> Сообщение ИИ для->   {user_name} ({user_id}): {response.text}")
    logs(user_id, user_name, f"{now_time()} -> Сообщение ИИ для-> {user_name} ({user_id}): {response.text}")
    return response.text
def user_access_list_gen(user_name_for_start, user_id, user_name):
    client = gemini_client
    config_plugins = plugins.get_plugins_config(user_id)
    if config_plugins["ai_commands"] == True:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=command_gen_prompts.user_access_list_gen_prompts),
            contents=f"Пользователь не получил ответа, сообщи ему почему, имя пользователя {user_name_for_start}.")
        print(f"{now_time()} -> Сообщение ИИ для->   {user_name} ({user_id}): {response.text}")
        logs(user_id, user_name, f"{now_time()} -> Сообщение ИИ для-> {user_name} ({user_id}): {response.text}")
        return response.text
    else: 
        return "У вас нет доступа к боту, свяжитесь с @WorldWideWebAdmin"
def error_message_gen(user_name_for_start, user_id, user_name):
    client = gemini_client
    config_plugins = plugins.get_plugins_config(user_id)
    if config_plugins["ai_commands"] == True:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=command_gen_prompts.error_message_gen_prompts),
            contents=f"Пользователь получил ошибку. Имя пользователя:  {user_name_for_start}.")
        print(f"{now_time()} -> Сообщение ИИ для->   {user_name} ({user_id}): {response.text}")
        logs(user_id, user_name, f"{now_time()} -> Сообщение ИИ для-> {user_name} ({user_id}): {response.text}")
        return response.text
    else:
        return "Возникла ошибка😭. Чат был сброшен."