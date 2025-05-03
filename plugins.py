import time
from config import conversations, ADMIN
import prompts
from aiogram import types, Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, BaseFilter
from aiogram.types import Message
from logs.logs import logs
import forai
plugins_configs = {}
def get_plugins_config(user_id: int):
    if user_id not in plugins_configs:
        plugins_configs[user_id] = {
            "ai_commands": False,
            "gemini_client": False
        }
    return plugins_configs[user_id]
plugins_router = Router()
def create_plugins_menu() -> InlineKeyboardBuilder:
    plugins_menu = InlineKeyboardBuilder()
    plugins_menu.row (types.InlineKeyboardButton(text="ИИ Команды", callback_data="AI_Commands"))
    plugins_menu.row(types.InlineKeyboardButton(text="Gemini Ai", callback_data="Gemini"))
    return plugins_menu

@plugins_router.message(Command("plugins"))
async def plugins_main_menu(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username or 'Unknown user'
    await message.answer ('Выберите плагин📦:', reply_markup=create_plugins_menu().as_markup())
    print(f"{forai.now_time()} -> /plugins ->   {user_name} ({user_id}):")
    logs(user_id, user_name, f"{forai.now_time()} -> /plugins ->   {user_name} ({user_id}):")

@plugins_router.callback_query(F.data == "AI_Commands")
async def ai_commands(callback: types.CallbackQuery):
    ai_commands_menu = InlineKeyboardBuilder()
    ai_commands_menu.row(types.InlineKeyboardButton(text="Включить🔛", callback_data="ai_commands_on"))
    ai_commands_menu.row(types.InlineKeyboardButton(text="Выключить📴", callback_data="ai_commands_off"))
    await callback.message.edit_text("Выберите действие👌:", reply_markup=ai_commands_menu.as_markup())
@plugins_router.callback_query(F.data == "ai_commands_on")
async def ai_commands_on(callback: types.CallbackQuery):
    config = get_plugins_config(callback.from_user.id)
    config["ai_commands"] = True
    await callback.message.edit_text("ИИ Команды включены😊", reply_markup=create_plugins_menu().as_markup())
    user_id = callback.from_user.id
    conversations[user_id] = []
    print(f"{forai.now_time()} -> AICommandsON ->   {callback.from_user.username} ({callback.from_user.id}):")
    logs(callback.from_user.id, callback.from_user.username, f"{forai.now_time()} -> AICommandsON ->   {callback.from_user.username} ({callback.from_user.id}):")
    await callback.answer()
    
@plugins_router.callback_query(F.data == "ai_commands_off")
async def ai_commands_off(callback: types.CallbackQuery):
    config = get_plugins_config(callback.from_user.id)
    config["ai_commands"] = False
    await callback.message.edit_text("ИИ Команды выключены😊", reply_markup=create_plugins_menu().as_markup())
    user_id = callback.from_user.id
    conversations[user_id] = []
    print(f"{forai.now_time()} -> AICommandsOFF ->   {callback.from_user.username} ({callback.from_user.id}):")
    logs(callback.from_user.id, callback.from_user.username, f"{forai.now_time()} -> AICommandsOFF ->   {callback.from_user.username} ({callback.from_user.id}):")
    await callback.answer()
@plugins_router.callback_query(F.data == "Gemini")
async def gemini_client(callback: types.CallbackQuery):
    gemini_client_menu = InlineKeyboardBuilder()
    gemini_client_menu.row(types.InlineKeyboardButton(text = "Включить 🔛", callback_data = "gemini_client_on"))
    gemini_client_menu.row(types.InlineKeyboardButton(text = "Выключить 📴", callback_data = "gemini_client_off"))
    await callback.message.edit_text("Выберите действие 👌:", reply_markup=gemini_client_menu.as_markup())
@plugins_router.callback_query(F.data == "gemini_client_on")
async def gemini_client_on(callback: types.CallbackQuery):
    config = get_plugins_config(callback.from_user.id)
    config["gemini_client"] = True
    await callback.message.edit_text("Gemini AI включена 😊", reply_markup=create_plugins_menu().as_markup())
    user_id = callback.from_user.id
    conversations[user_id] = []
    print(f"{forai.now_time()} -> GeminiAION ->   {callback.from_user.username} ({callback.from_user.id}):")
    logs(callback.from_user.id, callback.from_user.username, f"{forai.now_time()} -> GeminiAION ->   {callback.from_user.username} ({callback.from_user.id}):")
    await callback.answer()

@plugins_router.callback_query(F.data == "gemini_client_off")
async def gemini_client_off(callback: types.CallbackQuery):
    config = get_plugins_config(callback.from_user.id)
    config["gemini_client"] = False
    await callback.message.edit_text("Gemini AI выключена 😭", reply_markup=create_plugins_menu().as_markup())
    user_id = callback.from_user.id
    conversations[user_id] = []
    print(f"{forai.now_time()} -> GeminiAIOFF ->   {callback.from_user.username} ({callback.from_user.id}):")
    logs(callback.from_user.id, callback.from_user.username, f"{forai.now_time()} -> GeminiAIOFF ->   {callback.from_user.username} ({callback.from_user.id}):")
    await callback.answer()

