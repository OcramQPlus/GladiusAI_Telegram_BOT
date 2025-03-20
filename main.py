import asyncio
from config import GladiusAI, GladiusAI_Bot
import admin
import styles
import user_message
import commands
import feedback


async def main():
    GladiusAI.include_router(commands.commands)
    GladiusAI.include_router(admin.admin_router)
    GladiusAI.include_router(styles.styles)
    GladiusAI.include_router(feedback.feedback_router)
    GladiusAI.include_router(user_message.user_message_router)

    await GladiusAI.start_polling(GladiusAI_Bot)

if __name__ == "__main__":
    asyncio.run(main())
    GladiusAI.start_polling(GladiusAI) 