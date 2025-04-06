# Description: Модуль обработки сообщений от пользователя
# Импорт библиотек и файлов
from aiogram import Router, types
import admin
import feedback
from aiogram.filters import BaseFilter
import mistralaiclient
from aiogram.types import Message
import geminiaiclient
import config
import command_gen
import forai
from logs.logs import logs
# Создание роутера
user_message_router = Router()
# Обработка сообщений от пользователя
# Фильтр для проверки достуна
class Access_to_the_bot(BaseFilter):
    def __init__(self, user_access: list[int]):
        self.user_access = user_access
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.user_access
@user_message_router.message(Access_to_the_bot(user_access=config.user_access_list),)
async def user_message_get(message: types.Message):
    #Записываем логи
    user_name = message.from_user.username
    user_id = message.from_user.id
    print(f"{forai.now_time()} -> Пользователь получил доступ к боту->   {user_name} ({user_id}): {message.text}")
    logs(user_id, user_name, f"{forai.now_time()} -> Пользователь получил доступ к боту-> {user_name} ({user_id}): {message.text}")
    # Получаем конфигурацию пользователя
    config = admin.get_user_config(message.from_user.id)
    # Проверяем статус GladiusAI
    if admin.GladiusAI_status == False:
        await message.reply("""GladiusAI на данный момент не работает.
Попробуйте позже.😓""")
        return
    # Проверяем статус feedback
    if feedback.feedback_status == True:
        await feedback.feedback_message_write(message)
        feedback.feedback_status = False
        return
    # Проверяем выбраную ИИ
    match config["ai_right_now"]:
        case "mistral_ai_client":
            await mistralaiclient.mistral_answer(message)
            user_id = message.from_user.id
        case "gemini_ai_client":
            await geminiaiclient.gemini_answer(message)
            user_id = message.from_user.id
#У пользователя нет доступа к боту
@user_message_router.message()
async def user_message_get(message: types.Message):
    await message.reply(command_gen.user_access_list_gen(message.from_user.id, message.from_user.username, message.text or "Нет сообщения"))
    user_name = message.from_user.username
    user_id = message.from_user.id
    print(f"{forai.now_time()} -> Пользователь не получил доступа к боту->   {user_name} ({user_id}): {message.text}")
    logs(user_id, user_name, f"{forai.now_time()} -> Пользователь не получил доступа к боту-> {user_name} ({user_id}): {message.text}")