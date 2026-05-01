from aiogram.filters import Command
from aiogram import Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from services import load_users_data, load_reminds_data
import os

router = Router()

ADMIN_KEY = os.getenv("ADMIN_KEY", "ANY")

adminM = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Foydalanuvchilarni Ko'rish", callback_data="show_users")],
        [InlineKeyboardButton(text="Kalitni O'zgartirish", callback_data="change_key")],
    ]
)

class AdminState(StatesGroup):
    waiting_for_key = State()
    waiting_for_new_key = State()

@router.message(Command("admin"))
async def admin_command(message: types.Message, state: FSMContext):
    await message.answer("Admin paneliga kirish uchun kalitni yozing:")
    await state.set_state(AdminState.waiting_for_key)

@router.message(AdminState.waiting_for_key)
async def admin_key_check(message: types.Message, state: FSMContext):
    entered_key = message.text.strip()
    
    if entered_key == ADMIN_KEY:
        await message.answer("Xush kelibsiz, Admin!", reply_markup=adminM)
        await state.clear()
    else:
        await message.answer("Kalit noto'g'ri! Qayta urinib ko'ring.")

@router.callback_query(lambda c: c.data == "show_users")
async def show_users_handler(callback: CallbackQuery):
    users_data = load_users_data()
    
    if not users_data:
        await callback.message.answer("Hech qanday foydalanuvchi yo'q")
        return
    
    users_list = "📋 **Foydalanuvchilar ro'yxati:**\n\n"
    for user in users_data:
        user_id = user.get("user_id", "N/A")
        user_name = user.get("name", "N/A")
        users_list += f"🔹 ID: `{user_id}`\n   Ism: {user_name}\n"
    
    await callback.message.answer(users_list, parse_mode="Markdown")

@router.callback_query(lambda c: c.data == "change_key")
async def change_key_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Yangi kalitni yozing:")
    await state.set_state(AdminState.waiting_for_new_key)

@router.message(AdminState.waiting_for_new_key)
async def new_key_input(message: types.Message, state: FSMContext):
    new_key = message.text.strip()
    
    if len(new_key) < 4:
        await message.answer("Kalit kamida 4 ta belgi bo'lishi kerak. Qayta urinib ko'ring.")
        return
    
    with open(".env", "r") as f:
        env_content = f.read()
    
    if "ADMIN_KEY=" in env_content:
        env_content = env_content.split("ADMIN_KEY=")[0] + f"ADMIN_KEY={new_key}"
    else:
        env_content += f"\nADMIN_KEY={new_key}"
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    await message.answer(f"✅ Kalit muvaffaqiyatli o'zgartirildi!\nYangi kalit: `{new_key}`", parse_mode="Markdown")
    await state.clear()
