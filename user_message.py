# Description: Модуль обработки сообщений от пользователя
# Импорт библиотек и файлов
from aiogram import Router, types
import admin
import feedback
import mistralaiclient
import geminiaiclient
# Создание роутера
user_message_router = Router()
# Обработка сообщений от пользователя
@user_message_router.message()
async def user_message_get(message: types.Message):
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
            admin.conversations[user_id] = []
        case "gemini_ai_client":
            await geminiaiclient.gemini_answer(message)
            user_id = message.from_user.id
            admin.conversations[user_id] = []