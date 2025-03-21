# Description: Файл с командами бота
# Импорт библиотек и файлов
from aiogram import types, F, Router
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from config import conversations
import time
from logs.logs import logs
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
    # Приветствие пользователя
    user_name_for_start = message.from_user.first_name or ""
    await message.reply(f"""
Привет {user_name_for_start}! Я - Профессор физики Gladius👨‍🎓, помогу тебе с любыми вопросами по физике.
Что бы узнать боьше информации о боте, напиши /help    
                        """)
    print(f"{now_time()} -> /start ->   {user_name} ({user_id}):")
    logs (user_id, user_name, f"{now_time()} -> /start -> {user_name} ({user_id}):")
# Команда /clear
@commands.message(Command(("clear")))
async def clear_history(message: types.Message):
    user_name = message.from_user.username or "Unknown User"
    user_id = message.from_user.id
    # Очистка истории сообщений
    conversations[user_id] = []
    await message.reply("Память стёрта😓")
    print(f"{now_time()} -> /clear ->   {user_name} ({user_id}):")
    logs (user_id, user_name, f"{now_time()} -> /clear -> {user_name} ({user_id}):")
# Команда /help
@commands.message(F.text, Command(("help")))
async def send_help(message: types.Message):
    await message.answer("""
Наши команды:
    /start - Начать диалог с ботом
    /clear - Очистить историю сообщений
    /help - Помощь и информация по боту
    /style - Изменить стиль сообщений
    /admin - Панель администратора
На основе: <b>Mistral Ai</b>
Подерживаются только сообщения.
<span class=\"tg-spoiler\">Возможны ошибки</span>
                         """, parse_mode=ParseMode.HTML)
    user_id = message.from_user.id
    user_name = message.from_user.username or "Unknown User"
    print(f"{now_time()} -> /help ->   {user_name} ({user_id}):")
    logs (user_id, user_name, f"{now_time()} -> /help -> {user_name} ({user_id}):")
    
    

    
    
