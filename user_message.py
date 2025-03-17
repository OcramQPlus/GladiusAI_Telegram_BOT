from aiogram import Router, types

import admin
import feedback

import mistralaiclient
import geminiaiclient


user_message_router = Router()
@user_message_router.message()
async def user_message_get(message: types.Message):
    if admin.GladiusAI_status == False:
        await message.reply("""GladiusAI на данный момент не работает.
Попробуйте позже.😓""")
        return
    if feedback.feedback_status == True:
        await feedback.feedback_message_write(message)
        feedback.feedback_status = False
        return
    match admin.ai_right_now:
        case "mistralaiclient":
            await mistralaiclient.mistral_answer(message)
        case "geminiaiclient":
            await geminiaiclient.gemini_answer(message)
        