import asyncio
from datetime import datetime
from aiogram import Bot
from services import load_reminds_data

async def check_reminders(bot: Bot):
    while True:
        time = datetime.now().strftime("%H:%M")
        data = load_reminds_data()
        
        for user in data:
            for note_dict in user["time_notes"]:
                for k, v in note_dict.items():
                    if k == time:
                        await bot.send_message(
                            chat_id=user["user_id"],
                            text=f"🔔 Vaqt {k} bo'ldi, sizda '{v}' eslatma bor"
                        )
        
        await asyncio.sleep(60)  