from aiogram.filters import Command
from aiogram import Router, types
from services import save_user
router = Router()

@router.message(Command("start"))
async def command_start_handler(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!")
    save_user(message.from_user.id, message.from_user.full_name)