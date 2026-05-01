from aiogram.filters import Command
from aiogram import Router, types
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from services import load_reminds_data, save_note, save_note_time, check_time_format
router = Router()

optionM = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ha", callback_data="yes", style="success"),
            InlineKeyboardButton(text="Yoq", callback_data="no", style="danger"),
        ]
    ]
)


class wait_note(StatesGroup):
    waiting_for_noteName = State()
    waiting_for_time = State()
    waiting_for_time_note = State()

@router.message(Command("newnote"))
async def command_newNote_handler(message: types.Message, state: FSMContext):
    await message.answer("Eslatma uchun vaqt belgilaysizmi?", reply_markup=optionM)


@router.callback_query(lambda c: c.data == "no")
async def add_remind_wo_time(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Eslatmani Yozing... ")
    await state.set_state(wait_note.waiting_for_noteName)

@router.message(wait_note.waiting_for_noteName)
async def note_name(message: types.Message, state: FSMContext):
    r = save_note(message.text, message.from_user.id)
    if r:
        await message.answer("Eslatmangiz Saqlandi!")
    else:
        await message.answer("Eslatmangiz Saqlanmadi!")
    await state.clear()

@router.callback_query(lambda c: c.data == "yes")
async def add_remind_time(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Eslatmangiz uchun vaqt yozing masalan : 15:30")
    await state.set_state(wait_note.waiting_for_time)

@router.message(wait_note.waiting_for_time)
async def add_time_tonote(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)    
    await message.answer("Endi Eslatmani Yozing!")
    await state.set_state(wait_note.waiting_for_time_note)

@router.message(wait_note.waiting_for_time_note)
async def ask_note(message: types.Message, state: FSMContext):
    data = await state.get_data()
    time = data["time"]
    remind = message.text
    st = check_time_format(time)
    if st:
        save_note_time(remind, time, message.from_user.id)
        await message.answer(f"Muvaffaqiyatli Saqlandi, sizga {time} da '{remind}' habari eslatilinadi.\nMuhim: botni ovozsiz holatda bolmasligi kerak!")
    else:
        await message.answer("Eslatma Saqlanmadi,Soat formati noto'g'ri bo'lishi mumkin")

    await state.clear()



