# Description: Файл с командами бота
# Импорт библиотек и файлов
from aiogram import types, F, Router
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from config import conversations
import time
from logs.logs import logs
import admin
import prompts
import command_gen
import plugins
# Создание роутера
commands = Router()
# Функция для получения текущего времени
def now_time():
    curent_time = time.time()
    local_time = time.localtime(curent_time)
    format_time = time.strftime("[%D %H:%M:%S]", local_time)
    return format_time
# Команды бота
# Команда /start
@commands.message(Command(("start")))
async def send_welcome(message: types.Message):
    # Получение данных пользователя
    user_id = message.from_user.id
    user_name = message.from_user.username or "Unknown User"
    conversations[user_id] = []
    config_plugins = plugins.get_plugins_config(message.from_user.id)
    if config_plugins["ai_commands"] == True:
        # Приветствие пользователя
        await message.reply(f"{command_gen.start_message_gen(message.from_user.first_name or "Его нет",user_id, user_name)}")

    else:
        await message.reply("Привет, Matvey! 👋 Я Gladius, твой бот-помощник! Рад видеть тебя! 😉 Чтобы узнать, что я умею, жми /help 😉")
    print(f"{now_time()} -> /start ->   {user_name} ({user_id}):")
    logs (user_id, user_name, f"{now_time()} -> /start -> {user_name} ({user_id}):")
# Команда /clear
@commands.message(Command(("clear")))
async def clear_history(message: types.Message):
    user_name = message.from_user.username or "Unknown User"
    user_id = message.from_user.id
    # Очистка истории сообщений
    conversations[user_id] = []
    config_plugins = plugins.get_plugins_config(message.from_user.id)
    if config_plugins["ai_commands"] == True:
        await message.reply(f"{command_gen.clear_message_gen(user_id, user_name)}")
    else:
        await message.reply("Чат был очищен😊")
    print(f"{now_time()} -> /clear ->   {user_name} ({user_id}):")
    logs (user_id, user_name, f"{now_time()} -> /clear -> {user_name} ({user_id}):")
#Очистка/Сброс настроек пользователя
@commands.message(Command(("clear_settings")))
async def clear_settings(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username or "Unknown User"
    config = admin.get_user_config(message.from_user.id)
    config["ai_right_now"] = "mistral_ai_client"
    config["default_prompts"] = prompts.physical_prompt
    config["mistral_model"] = "mistral-large-latest"
    config["gemini_model"] = "gemini-2.0-flash"
    config["debug_mode"] = False
    conversations[user_id] = []
    config_plugins = plugins.get_plugins_config(message.from_user.id)
    if config_plugins["ai_commands"] == True:
        await message.reply(f"{command_gen.clear_settings_message_gen(user_id, user_name)}")
        config_plugins["ai_commands"] = False
    else:
        await message.reply("Настройки были сброшены😊")
    print(f"{now_time()} -> /clear_settings ->   {message.from_user.username or 'Unknown User'} ({user_id}):")
    logs (user_id, message.from_user.username or 'Unknown User', f"{now_time()} -> /clear_settings -> {message.from_user.username or 'Unknown User'} ({user_id}):")
# Команда /help
@commands.message(F.text, Command(("help")))
async def send_help(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username or "Unknown User"
    config_plugins = plugins.get_plugins_config(message.from_user.id)
    if config_plugins["ai_commands"] == True:
        await message.answer(f"{command_gen.help_message_gen(message.from_user.first_name or "Его нет",user_id,user_name)}")
    else:
        await message.answer("""
Привет, Matvey! 👋 Я Gladius, твой бот-помощник с искусственным интеллектом! 🤖

Вот что я умею:

/start - Начнём общение! 🚀
/clear - Очистим историю сообщений, чтобы начать с чистого листа! 🧹
/help - Ты уже здесь! 😉 Расскажу о себе и командах.
/clear_settings - Сбросим все настройки к заводским! ⚙️
/admin - Панель для избранных! 👑 (Чтобы получить доступ, напиши @No0160)
/feedback - Есть идеи или отзывы? Я весь внимание! 📝
/plugins - Включить плагины для бота 📦!

Я создан на основе Mistral Ai и Gemini Ai, поэтому могу отвечать на вопросы на любые темы! 🧠 Просто напиши мне что-нибудь! 🗣️

Важно: Я работаю на ИИ, поэтому иногда могу ошибаться. 😅

Чтобы получить доступ к общению со мной, напиши @WorldWideWebAdmin! ✍️

Подписывайся на мой канал: @GladiusAI! 📣

Зацени мой код: https://github.com/OcramQPlus/GladiusAI_Telegram_BOT! 💻

Разработчик: @No0160 👨‍💻

Все ответы, даже этот, сгенерированы ИИ! 🤯""")
    print(f"{now_time()} -> /help ->   {user_name} ({user_id}):")
    logs (user_id, user_name, f"{now_time()} -> /help -> {user_name} ({user_id}):")
    
    

    
    
