# Description: файл запуска бота
# Импорт библиотек и файлов
import asyncio
from config import GladiusAI, GladiusAI_Bot
import admin
import user_message
import commands
import feedback
import plugins
#UTF-8
import sys
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='UTF-8', buffering=1)
sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='UTF-8', buffering=1)
# Основная функция
async def main():
    GladiusAI.include_router(commands.commands)
    GladiusAI.include_router(admin.admin_router)
    GladiusAI.include_router(plugins.plugins_router)
    GladiusAI.include_router(feedback.feedback_router)
    GladiusAI.include_router(user_message.user_message_router)
    await GladiusAI.start_polling(GladiusAI_Bot)
# Запуск основной функции
if __name__ == "__main__":
    asyncio.run(main())