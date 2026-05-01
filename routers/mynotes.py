from aiogram.filters import Command
from aiogram import Router, types
from services import load_reminds_data
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
router = Router()


@router.message(Command("mynotes"))
async def command_start_handler(message: types.Message):
    data = load_reminds_data()
    for i in data:
        if i["user_id"] == message.from_user.id:
            if len(i["notes"])==0 and len(i["time_notes"])==0:
                await message.answer("Sizda hali Eslatma mavjud emas!")
            if len(i["notes"])!=0:
                await message.answer("Sizning Eslatmalaringiz!"+ f" soni {len(i["notes"])}ta")
                res = ""
                for j in range(1, len(i["notes"])+1):
                    # await message.answer(f"{j}: {i["notes"][j]}")
                    res = res+"".join(f"{j} : {i["notes"][j-1]}\n")
                await message.answer(res)
                # //////////////////////////////////////////////////////////////////////////////////////
            if len(i["time_notes"])!=0:
                await message.answer("Sizning Vaqtli Eslatmalaringiz"+ f" soni {len(i["time_notes"])}ta")
                res = ""
                for n in range(1, len(i["time_notes"])+1):
                    for k, v in i["time_notes"][n-1].items(): 
                        res = res+"".join(f"{k} : {v}\n")
                await message.answer(res)    





