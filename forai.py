# Description: Файл с общими функциями для бота
# Импорт библиотек
from random import choice
import time
# Переменные
last_request_time = {}
RATE_LIMIT = 2
# Текущее время 
def now_time():
    curent_time = time.time()
    local_time = time.localtime(curent_time)
    format_time = time.strftime("[%D %H:%M:%S]", local_time)
    return format_time
# Генератор сообщения ожидания
def waiting_response_generator():
    waiting_responses = [
        "Подожди немного, готовим ответ 🤗",
        "Нам нужно немного времени 🕗", 
        "Спрашивем у всевидящего каркозлика 🐐!",
        "Спрашиваем у мудреца Ли Вэйя и его правой руки Син Цзуна 👴.",
        "Неть-ниндзя говорит что ты не получишь ответа! 😑",
        "Изучаем информацию для лучшего ответа 📚",
        "Это не займет много времени 😴",
        "Скоро ответим 🥳",
        "Генерация... 🤖",
        "Ищем новые идеи для лучшего результата 💡",
        "Пишем ответ вручную(нет) 👨‍💻",
        "Подождите, мы не успеваем 🤔",
        "Одно мгновение 🏎",
        "Анализируем базы данных 🔍",
        "Поиск информации в сети... 🌐",
        "Подбираем лучший ответ для вас 😘",
        "Проверяем информацию на достоверность 📝",
        "Обрабатываем ваш запрос... 💻",
        "Ищем в Google... 🙄",
        "Ищем в Яндексе... 🤔",
        "Спрашиваем у прохожих 🤷‍♂️",
        "Проводим опрос на лучший ответ 📊",
        "Смотрим в будущее... 🔮",
        "Надеюсь я не забыл про тебя 🤭",
        "Смотрим в прошлое... 🕰",
        "Надеюсь, это не займет много времени 😓",
        "А не много ли ты спрашиваешь? 🤨",
        "Работаю за кошка-девочка и миска риса🍚",
        "Я уже запутался в твоих запросах 📴",
        "Скоро будет ошибка! 💥 (нет)"
    ]
    return choice(waiting_responses)