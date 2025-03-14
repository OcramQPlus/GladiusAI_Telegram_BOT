import time



from config import conversations

from aiogram import types, Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from aiogram.filters import BaseFilter
from aiogram.types import Message

from config import ADMIN
import prompts

from logs.logs import logs
admin_router = Router()
model = "mistral-large-latest"
GladiusAI_status = True

def now_time():
    curent_time = time.time()
    local_time = time.localtime(curent_time)
    format_time = time.strftime("[%D %H:%M:%S]", local_time)
    return format_time


class IsAdminFilter(BaseFilter):
    def __init__(self, admin_ids: list[int]):
        self.admin_ids = admin_ids
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids
    
@admin_router.message(IsAdminFilter(admin_ids=ADMIN), Command(("admin")))
async def admin_command(message: types.Message):
    global admin_menu
    admin_menu = InlineKeyboardBuilder()
    admin_menu.row (types.InlineKeyboardButton(text="Выбор персонажа 👨‍👩‍👧‍👦", callback_data="promt_choose_admin"),)
    admin_menu.row (types.InlineKeyboardButton(text="Изменить языковую модель 👤", callback_data="model_selection_admin"),)
    admin_menu.row (types.InlineKeyboardButton(text="Отладка 🛠", callback_data="debug"),)
    admin_menu.row (types.InlineKeyboardButton(text="ON and OFF 🛑", callback_data="on_off"),)
    admin_menu.row (types.InlineKeyboardButton(text="Удалить это сообщение 💥", callback_data="del_admin_menu"),)
    await message.answer("Выберите действие 🧩", reply_markup=admin_menu.as_markup())
    user_id = message.from_user.id
    user_name = message.from_user.username or "Unknown User"
    print (f"{now_time()} -> /admin ->   {user_name} ({user_id}):")
    logs (user_id, user_name, f"{now_time()} -> /admin ->   {user_name} ({user_id}):")
    
@admin_router.message(Command("admin"))
async def not_admin(message: types.Message):
    await message.reply("У вас нет прав администратора 🚫")
    user_id = message.from_user.id
    user_name = message.from_user.username or "Unknown User"
    print (f"{now_time()} -> /admin ->   {user_name} ({user_id}):")
    logs (user_id, user_name, f"{now_time()} -> /admin ->   {user_name} ({user_id}):")
    
@admin_router.callback_query(F.data == "on_off")
async def on_off(callback: types.CallbackQuery):
    on_off_menu = InlineKeyboardBuilder()
    on_off_menu.row (types.InlineKeyboardButton(text="Включить 💡", callback_data="on"),)
    on_off_menu.row (types.InlineKeyboardButton(text="Выключить 🔌", callback_data="off"),)
    on_off_menu.row (types.InlineKeyboardButton(text="Назад ↩", callback_data="back_to_admin_menu"),)
    await callback.message.edit_text("Выберите действие 👀", reply_markup=on_off_menu.as_markup())
    await callback.answer()
    
    
@admin_router.callback_query(F.data == "on")
async def on(callback: types.CallbackQuery):
    global GladiusAI_status
    GladiusAI_status = True
    await callback.message.edit_text("Включено 💡",reply_markup=admin_menu.as_markup())
    await callback.answer()
@admin_router.callback_query(F.data == "off")
async def off(callback: types.CallbackQuery):
    global GladiusAI_status
    GladiusAI_status = False
    await callback.message.edit_text("Выключено 🔌",reply_markup=admin_menu.as_markup())
    await callback.answer()
@admin_router.callback_query(F.data == "back_to_admin_menu")
async def back_to_admin_menu(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите действие 🧩", reply_markup=admin_menu.as_markup())
    await callback.answer()
debug_mode = False
@admin_router.callback_query(F.data == "debug")
async def debug(callback: types.CallbackQuery):
    debug_menu = InlineKeyboardBuilder()
    debug_menu.row (types.InlineKeyboardButton(text="Включить 💉", callback_data="debug_on"),)
    debug_menu.row (types.InlineKeyboardButton(text="Выключить 🧫", callback_data="debug_off"),)
    debug_menu.row (types.InlineKeyboardButton(text="Назад ↩", callback_data="back_to_admin_menu"),)
    await callback.message.edit_text("Выберите действие 👀", reply_markup=debug_menu.as_markup())
    await callback.answer()
@admin_router.callback_query(F.data == "debug_on")
async def debug_on(callback: types.CallbackQuery):
    global debug_mode
    debug_mode = True
    await callback.message.edit_text("Отладка включена 🧰",reply_markup=admin_menu.as_markup())
@admin_router.callback_query(F.data == "debug_off")
async def debug_user_off(callback: types.CallbackQuery):
    global debug_mode
    debug_mode = False
    await callback.message.edit_text("Отладка выключена ⚰",reply_markup=admin_menu.as_markup())

@admin_router.callback_query(F.data == "del_admin_menu")
async def del_admin_menu(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.answer()
    

@admin_router.callback_query(F.data == "model_selection_admin")
async def model_selection_admin(callback: types.CallbackQuery):
    model_selection = InlineKeyboardBuilder()
    model_selection.row (types.InlineKeyboardButton(text="pixtral-large-latest", callback_data="pixtral_large_latest"),)
    model_selection.row (types.InlineKeyboardButton(text="ministral-8b-latest", callback_data="ministral_8b_latest"),)
    model_selection.row (types.InlineKeyboardButton(text="mistral-large-latest", callback_data="mistral-large-latest"),)
    model_selection.row (types.InlineKeyboardButton(text="ministral-3b-latest", callback_data="ministral_3b_latest"),)
    model_selection.row (types.InlineKeyboardButton(text="pixtral-12b-2409", callback_data="pixtral_12b_2409"),)
    model_selection.row (types.InlineKeyboardButton(text="Назад ↩", callback_data="back_to_admin_menu"),)
    await callback.message.edit_text("Выберите языковую модель:", reply_markup=model_selection.as_markup())
@admin_router.callback_query(F.data == "pixtral_large_latest")
async def pixtral_large_latest(callback: types.CallbackQuery):
    global model
    model = "pixtral-large-latest"
    await callback.message.edit_text("Выбранная модель: pixtral-large-latest",reply_markup=admin_menu.as_markup())

@admin_router.callback_query(F.data == "ministral_8b_latest")
async def ministral_8b_latest(callback: types.CallbackQuery):
    global model
    model = "ministral-8b-latest"
    await callback.message.edit_text("Выбранная модель: ministral-8b-latest",reply_markup=admin_menu.as_markup())
@admin_router.callback_query(F.data == "mistral-large-latest") 
async def mistral_large_latest(callback: types.CallbackQuery):
    global model
    model = "mistral-large-latest"
    await callback.message.edit_text("Выбранная модель: mistral-large-latest",reply_markup=admin_menu.as_markup())
@admin_router.callback_query(F.data == "ministral_3b_latest")
async def ministral_3b_latest(callback: types.CallbackQuery):
    global model
    model = "ministral-3b-latest"
    await callback.message.edit_text("Выбранная модель: ministral-3b-latest",reply_markup=admin_menu.as_markup())
@admin_router.callback_query(F.data == "pixtral_12b_2409")
async def pixtral_12b_2409(callback: types.CallbackQuery):
    global model
    model = "pixtral-12b-2409"
    await callback.message.edit_text("Выбранная модель: pixtral-12b-2409",reply_markup=admin_menu.as_markup())


@admin_router.callback_query(F.data == "promt_choose_admin")
async def promt_choose_admin(callback: types.CallbackQuery):
    promt_selection = InlineKeyboardBuilder()
    promt_selection.row (types.InlineKeyboardButton(text="Девочка 🎀", callback_data="girl"),)
    promt_selection.row (types.InlineKeyboardButton(text="Мальчик 💪", callback_data="boy"),)
    promt_selection.row (types.InlineKeyboardButton(text="Злодей 😈", callback_data="villain"),)
    promt_selection.row (types.InlineKeyboardButton(text="Стандарт 🙂", callback_data="standart"),)
    promt_selection.row (types.InlineKeyboardButton(text="Профессор Физики 🧠", callback_data="physical"),)
    promt_selection.row (types.InlineKeyboardButton(text="Случайный 🎰", callback_data="random"),)
    promt_selection.row (types.InlineKeyboardButton(text="Назад ↩", callback_data="back_to_admin_menu"),)
    await callback.message.edit_text("Выбор персонажа:", reply_markup=promt_selection.as_markup())
@admin_router.callback_query(F.data == "girl")
async def girl(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    conversations[user_id] = [{"role": "user", "content": prompts.girl_prompt}]  
    await callback.message.edit_text("Ответы будут в стиле девочки🎀",reply_markup=admin_menu.as_markup())

@admin_router.callback_query(F.data == "boy")
async def boy(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    conversations[user_id] = [{"role": "user", "content": prompts.boy_prompt}]  
    await callback.message.edit_text("Ответы будут в стиле мальчика🏋️‍♀️",reply_markup=admin_menu.as_markup())

@admin_router.callback_query(F.data == "villain")
async def villain(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    conversations[user_id] = [{"role": "user", "content": prompts.villain_prompt}]
    await callback.message.edit_text("Ответы будут в стиле злодея😈",reply_markup=admin_menu.as_markup())

@admin_router.callback_query(F.data == "standart")
async def standart(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    conversations[user_id] = [{"role": "user", "content": prompts.standart_prompt}]
    await callback.message.edit_text("Ответы будут в обычном стиле🤖",reply_markup=admin_menu.as_markup())

@admin_router.callback_query(F.data == "physical")
async def standart (callback: types.CallbackQuery):
    user_id = callback.from_user.id
    conversations[user_id] = [{"role": "user", "content": prompts.physical_prompt}]
    await callback.message.edit_text("Ответы будут в стиле профессора физики👨‍🏫",reply_markup=admin_menu.as_markup())

@admin_router.callback_query(F.data == "random")
async def random(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    conversations[user_id] = [{"role": "user", "content": prompts.random_prompt}]
    await callback.message.edit_text("Ответы будут в случайном стиле🎰",reply_markup=admin_menu.as_markup())

    
    
    
