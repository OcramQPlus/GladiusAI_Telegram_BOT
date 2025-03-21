# Description: Модуль администратора, включает в себя все функции и команды для администратора бота.
# Импорт библиотек и файлов
import time
from config import conversations, ADMIN
import prompts
from aiogram import types, Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, BaseFilter
from aiogram.types import Message
from logs.logs import logs
# Создание роутера
admin_router = Router()
# Глобальная переменная для включения и выключения бота
GladiusAI_status = True
# Глобальный словарь с персональными настройками пользователей
user_configs = {}
def get_user_config(user_id: int):
    if user_id not in user_configs:
        user_configs[user_id] = {
            "ai_right_now": "mistral_ai_client",
            "default_prompts": prompts.physical_prompt,
            "mistral_model": "mistral-large-latest",
            "gemini_model": "gemini-2.0-flash",
            "debug_mode": False,
        }
    return user_configs[user_id]
# Функция для получения текущего времени
def now_time():
    curent_time = time.time()
    local_time = time.localtime(curent_time)
    format_time = time.strftime("[%D %H:%M:%S]", local_time)
    return format_time
# Фильтр для проверки администратора
class IsAdminFilter(BaseFilter):
    def __init__(self, admin_ids: list[int]):
        self.admin_ids = admin_ids
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids
# Функция для создания меню администратора
def create_admin_menu() -> InlineKeyboardBuilder:
    admin_menu = InlineKeyboardBuilder()
    admin_menu.row(types.InlineKeyboardButton(text="Выбор персонажа 👨‍👩‍👧‍👦", callback_data="promt_choose_admin"))
    admin_menu.row(types.InlineKeyboardButton(text="Изменить языковую модель 👤", callback_data="model_selection_admin"))
    admin_menu.row(types.InlineKeyboardButton(text="Отладка 🛠", callback_data="debug"))
    admin_menu.row(types.InlineKeyboardButton(text="ON and OFF 🛑", callback_data="on_off"))
    admin_menu.row(types.InlineKeyboardButton(text="Выбрать ИИ 🤖", callback_data="ai_choose"))
    admin_menu.row(types.InlineKeyboardButton(text="Удалить это сообщение 💥", callback_data="del_admin_menu"))
    return admin_menu
# Обработка команды администратора
@admin_router.message(IsAdminFilter(admin_ids=ADMIN), Command(("admin")))
async def admin_command(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username or "Unknown User"
    # Получаем персональную конфигурацию пользователя
    config = get_user_config(user_id)
    await message.answer("Выберите действие 🧩", reply_markup=create_admin_menu().as_markup())
    print(f"{now_time()} -> /admin ->   {user_name} ({user_id}):")
    logs(user_id, user_name, f"{now_time()} -> /admin ->   {user_name} ({user_id}):")
# Если прав администратора нет
@admin_router.message(Command("admin"))
async def not_admin(message: types.Message):
    await message.reply("У вас нет прав администратора 🚫")
    user_id = message.from_user.id
    user_name = message.from_user.username or "Unknown User"
    print(f"{now_time()} -> /admin ->   {user_name} ({user_id}):")
    logs(user_id, user_name, f"{now_time()} -> /admin ->   {user_name} ({user_id}):")
# Выбор ИИ
@admin_router.callback_query(F.data == "ai_choose")
async def ai_choose(callback: types.CallbackQuery):
    ai_choose_kb = InlineKeyboardBuilder()
    ai_choose_kb.row(types.InlineKeyboardButton(text="MistralAI 🌪", callback_data="mistralai"))
    ai_choose_kb.row(types.InlineKeyboardButton(text="GeminiAI 🌌", callback_data="geminiai"))
    ai_choose_kb.row(types.InlineKeyboardButton(text="Назад ↩", callback_data="back_to_admin_menu"))
    await callback.message.edit_text("Выберите ИИ 🤖:", reply_markup=ai_choose_kb.as_markup())
    await callback.answer()
# Выбор MistralAI
@admin_router.callback_query(F.data == "mistralai")
async def mistralai(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["ai_right_now"] = "mistral_ai_client"
    await callback.message.edit_text("Выбран MistralAI 🌪", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
# Выбор GeminiAI
@admin_router.callback_query(F.data == "geminiai")
async def geminiai(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["ai_right_now"] = "gemini_ai_client"
    await callback.message.edit_text("Выбран GeminiAI 🌌", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
# Включение и выключение бота
@admin_router.callback_query(F.data == "on_off")
async def on_off(callback: types.CallbackQuery):
    on_off_menu = InlineKeyboardBuilder()
    on_off_menu.row(types.InlineKeyboardButton(text="Включить 💡", callback_data="on"))
    on_off_menu.row(types.InlineKeyboardButton(text="Выключить 🔌", callback_data="off"))
    on_off_menu.row(types.InlineKeyboardButton(text="Назад ↩", callback_data="back_to_admin_menu"))
    await callback.message.edit_text("Выберите действие 👀", reply_markup=on_off_menu.as_markup())
    await callback.answer()
# Включение бота
@admin_router.callback_query(F.data == "on")
async def on(callback: types.CallbackQuery):
    global GladiusAI_status
    GladiusAI_status = True
    await callback.message.edit_text("Включено 💡", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
# Выключение бота
@admin_router.callback_query(F.data == "off")
async def off(callback: types.CallbackQuery):
    global GladiusAI_status
    GladiusAI_status = False
    await callback.message.edit_text("Выключено 🔌", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
# Возврат в меню администратора
@admin_router.callback_query(F.data == "back_to_admin_menu")
async def back_to_admin_menu(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите действие 🧩", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
# Отладка
@admin_router.callback_query(F.data == "debug")
async def debug(callback: types.CallbackQuery):
    debug_menu = InlineKeyboardBuilder()
    debug_menu.row(types.InlineKeyboardButton(text="Включить 💉", callback_data="debug_on"))
    debug_menu.row(types.InlineKeyboardButton(text="Выключить 🧫", callback_data="debug_off"))
    debug_menu.row(types.InlineKeyboardButton(text="Назад ↩", callback_data="back_to_admin_menu"))
    await callback.message.edit_text("Выберите действие 👀", reply_markup=debug_menu.as_markup())
    await callback.answer()
# Включение отладки
@admin_router.callback_query(F.data == "debug_on")
async def debug_on(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["debug_mode"] = True
    await callback.message.edit_text("Отладка включена 🧰", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
# Выключение отладки
@admin_router.callback_query(F.data == "debug_off")
async def debug_off(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["debug_mode"] = False
    await callback.message.edit_text("Отладка выключена ⚰", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
# Удаление меню администратора
@admin_router.callback_query(F.data == "del_admin_menu")
async def del_admin_menu(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.answer()
# Выбор языковой модели
@admin_router.callback_query(F.data == "model_selection_admin")
async def model_selection_admin(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    model_selection = InlineKeyboardBuilder()
    # Выбор языковой модели для MistralAI
    if config["ai_right_now"] == "mistral_ai_client":
        model_selection.row(types.InlineKeyboardButton(text="pixtral-large-latest", callback_data="pixtral_large_latest"))
        model_selection.row(types.InlineKeyboardButton(text="ministral-8b-latest", callback_data="ministral_8b_latest"))
        model_selection.row(types.InlineKeyboardButton(text="mistral-large-latest", callback_data="mistral-large-latest"))
        model_selection.row(types.InlineKeyboardButton(text="ministral-3b-latest", callback_data="ministral_3b_latest"))
        model_selection.row(types.InlineKeyboardButton(text="pixtral-12b-2409", callback_data="pixtral_12b_2409"))
        model_selection.row(types.InlineKeyboardButton(text="Назад ↩", callback_data="back_to_admin_menu"))
        await callback.message.edit_text("Выберите языковую модель:", reply_markup=model_selection.as_markup())
    # Выбор языковой модели для GeminiAI
    if config["ai_right_now"] == "gemini_ai_client":
        model_selection.row(types.InlineKeyboardButton(text="gemini-2.0-flash", callback_data="gemini_2.0_flash"))
        model_selection.row(types.InlineKeyboardButton(text="gemini-2.0-flash-lite", callback_data="gemini_2.0_flash_lite"))
        model_selection.row(types.InlineKeyboardButton(text="gemini-2.0-pro-exp-02-05", callback_data="gemini_2.0_pro_exp_02_05"))
        model_selection.row(types.InlineKeyboardButton(text="gemini-1.5-flash", callback_data="gemini_1.5_flash"))
        model_selection.row(types.InlineKeyboardButton(text="gemini-1.5-flash-8b", callback_data="gemini_1.5_flash_8b"))
        model_selection.row(types.InlineKeyboardButton(text="gemini-1.5-pro", callback_data="gemini_1.5_pro"))
        model_selection.row(types.InlineKeyboardButton(text="Назад ↩", callback_data="back_to_admin_menu"))
        await callback.message.edit_text("Выберите языковую модель:", reply_markup=model_selection.as_markup())
# Выбор языковой модели для GeminiAI
@admin_router.callback_query(F.data == "gemini_2.0_flash")
async def gemini_2_0_flash(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["gemini_model"] = "gemini-2.0-flash"
    await callback.message.edit_text("Выбранная модель: gemini-2.0-flash", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
@admin_router.callback_query(F.data == "gemini_2.0_flash_lite")
async def gemini_2_0_flash_lite(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["gemini_model"] = "gemini-2.0-flash-lite"
    await callback.message.edit_text("Выбранная модель: gemini-2.0-flash-lite", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
@admin_router.callback_query(F.data == "gemini_2.0_pro_exp_02_05")
async def gemini_2_0_pro_exp_02_05(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["gemini_model"] = "gemini-2.0-pro-exp-02-05"
    await callback.message.edit_text("Выбранная модель: gemini-2.0-pro-exp-02-05", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
@admin_router.callback_query(F.data == "gemini_1.5_flash")
async def gemini_1_5_flash(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["gemini_model"] = "gemini-1.5-flash"
    await callback.message.edit_text("Выбранная модель: gemini-1.5-flash", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
@admin_router.callback_query(F.data == "gemini_1.5_flash_8b")
async def gemini_1_5_flash_8b(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["gemini_model"] = "gemini-1.5-flash-8b"
    await callback.message.edit_text("Выбранная модель: gemini-1.5-flash-8b", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
@admin_router.callback_query(F.data == "gemini_1.5_pro")
async def gemini_1_5_pro(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["gemini_model"] = "gemini-1.5-pro"
    await callback.message.edit_text("Выбранная модель: gemini-1.5-pro", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
# Выбор языковой модели для MistralAI
@admin_router.callback_query(F.data == "pixtral_large_latest")
async def pixtral_large_latest(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["mistral_model"] = "pixtral-large-latest"
    await callback.message.edit_text("Выбранная модель: pixtral-large-latest", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
@admin_router.callback_query(F.data == "ministral_8b_latest")
async def ministral_8b_latest(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["mistral_model"] = "ministral-8b-latest"
    await callback.message.edit_text("Выбранная модель: ministral-8b-latest", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
@admin_router.callback_query(F.data == "mistral-large-latest")
async def mistral_large_latest(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["mistral_model"] = "mistral-large-latest"
    await callback.message.edit_text("Выбранная модель: mistral-large-latest", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
@admin_router.callback_query(F.data == "ministral_3b_latest")
async def ministral_3b_latest(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["mistral_model"] = "ministral-3b-latest"
    await callback.message.edit_text("Выбранная модель: ministral-3b-latest", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
@admin_router.callback_query(F.data == "pixtral_12b_2409")
async def pixtral_12b_2409(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["mistral_model"] = "pixtral-12b-2409"
    await callback.message.edit_text("Выбранная модель: pixtral-12b-2409", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
# Выбор персонажа
@admin_router.callback_query(F.data == "promt_choose_admin")
async def promt_choose_admin(callback: types.CallbackQuery):
    promt_selection = InlineKeyboardBuilder()
    promt_selection.row(types.InlineKeyboardButton(text="Девочка 🎀", callback_data="girl"))
    promt_selection.row(types.InlineKeyboardButton(text="Мальчик 💪", callback_data="boy"))
    promt_selection.row(types.InlineKeyboardButton(text="Злодей 😈", callback_data="villain"))
    promt_selection.row(types.InlineKeyboardButton(text="Стандарт 🙂", callback_data="standart"))
    promt_selection.row(types.InlineKeyboardButton(text="Профессор Физики 🧠", callback_data="physical"))
    promt_selection.row(types.InlineKeyboardButton(text="Случайный 🎰", callback_data="random"))
    promt_selection.row(types.InlineKeyboardButton(text="Назад ↩", callback_data="back_to_admin_menu"))
    await callback.message.edit_text("Выбор персонажа:", reply_markup=promt_selection.as_markup())
    await callback.answer()
# Выбор стиля девочки
@admin_router.callback_query(F.data == "girl")
async def girl(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["default_prompts"] = prompts.girl_prompt
    await callback.message.edit_text("Ответы будут в стиле девочки🎀", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
# Выбор стиля мальчика
@admin_router.callback_query(F.data == "boy")
async def boy(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["default_prompts"] = prompts.boy_prompt
    await callback.message.edit_text("Ответы будут в стиле мальчика🏋️‍♀️", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
# Выбор стиля злодея
@admin_router.callback_query(F.data == "villain")
async def villain(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["default_prompts"] = prompts.villain_prompt
    await callback.message.edit_text("Ответы будут в стиле злодея😈", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
# Выбор стандартного стиля
@admin_router.callback_query(F.data == "standart")
async def standart(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["default_prompts"] = prompts.standart_prompt
    await callback.message.edit_text("Ответы будут в обычном стиле🤖", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
# Выбор стиля профессора физики
@admin_router.callback_query(F.data == "physical")
async def physical(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["default_prompts"] = prompts.physical_prompt
    await callback.message.edit_text("Ответы будут в стиле профессора физики👨‍🏫", reply_markup=create_admin_menu().as_markup())
    await callback.answer()
# Выбор случайного стиля
@admin_router.callback_query(F.data == "random")
async def random(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    config = get_user_config(user_id)
    config["default_prompts"] = prompts.random_prompt
    await callback.message.edit_text("Ответы будут в случайном стиле🎰", reply_markup=create_admin_menu().as_markup())
    await callback.answer()