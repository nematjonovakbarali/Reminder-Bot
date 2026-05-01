from aiogram.filters import Command
from aiogram import Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from services import load_reminds_data, remove_note as remove_note_service, clear_notes, remove_note_time
router = Router()

optionM = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Eslatmalar", callback_data="reminds", style="success")],
        [InlineKeyboardButton(text="Vaqt qo'yilgan eslatmalar", callback_data="reminds_time", style="primary")],
        [InlineKeyboardButton(text="Barcha Eslatmalarni o'chirish", callback_data="clear_notes", style="danger")],
    ]
)

class waiting_id(StatesGroup):
    waiting_for_regular_id = State()
    waiting_for_time_id = State()

@router.message(Command("removenote"))
async def remove_note(message: types.Message):
    await message.answer("Qaysi Bo'limdagi Eslatmani O'chirmoqchisiz", reply_markup=optionM)

@router.callback_query(lambda c: c.data == "reminds")
async def remove_reminds(callback: CallbackQuery, state: FSMContext):
    data = load_reminds_data()
    for i in data:
        if i["user_id"] == callback.from_user.id:
            if len(i["notes"])!=0:
                await callback.message.answer("Sizning Eslatmalaringiz!"+ f" soni {len(i["notes"])}ta")
                res = ""
                for j in range(1, len(i["notes"])+1):
                    res = res+"".join(f"{j} : {i["notes"][j-1]}\n")
                await callback.message.answer(res)
                await callback.message.answer("O'chirmoqchi bo'lgan eslatmangizni idsini yozing")
                await state.set_state(waiting_id.waiting_for_regular_id)
            else:
                await callback.message.answer("Sizda hali eslatma mavjud emas")


@router.message(waiting_id.waiting_for_regular_id)
async def remove_note_state(message: types.Message, state: FSMContext):
    text = message.text.strip()
    id_d = message.from_user.id
    res = remove_note_service(id_d, text)
    await state.clear()

    if res:
        await message.answer("Eslatma Ochirildi")
    else:
        await message.answer("Eslatma ochirilmadi, xatolik bo'lishi mumkin.\nIltimos, faol eslatma ID sini raqam sifatida kiriting va qayta urinib ko'ring.")




@router.callback_query(lambda c: c.data == "clear_notes")
async def clear_notes_handler(callback: CallbackQuery):
    a = clear_notes(callback.from_user.id)
    if a:
        await callback.message.answer("Barcha Eslatmalar O'chirildi!" )
    else:
        await callback.message.answer("Eslatmalar ochirilmadi")





@router.callback_query(lambda c: c.data == "reminds_time")
async def remove_time_reminds(callback: CallbackQuery, state: FSMContext):
    data = load_reminds_data()
    for i in data:
        if i["user_id"] == callback.from_user.id:
            if len(i["time_notes"])!=0:
                await callback.message.answer("Sizning Vaqtli Eslatmalaringiz!"+ f" soni {len(i["time_notes"])}ta")
                res = ""
                for j in range(1, len(i["time_notes"])+1):
                    time_note = i["time_notes"][j-1]
                    time, note = list(time_note.items())[0]
                    res += f"{j} : {time} - {note}\n"
                await callback.message.answer(res)
                await callback.message.answer("O'chirmoqchi bo'lgan eslatmangizni idsini yozing")
                await state.set_state(waiting_id.waiting_for_time_id)
            else:
                await callback.message.answer("Sizda hali eslatma mavjud emas")


@router.message(waiting_id.waiting_for_time_id)
async def remove_note_time_state(message: types.Message, state: FSMContext):
    text = message.text.strip()
    id_d = message.from_user.id
    res = remove_note_time(id_d, text)
    await state.clear()

    if res:
        await message.answer("Eslatma Ochirildi")
    else:
        await message.answer("Eslatma ochirilmadi, xatolik bo'lishi mumkin.\nIltimos, faol eslatma ID sini raqam sifatida kiriting va qayta urinib ko'ring.")




