import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from routers import start, mynotes, newnote, removenote, admin
from routers.reminder import check_reminders
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(start.router)
    dp.include_router(mynotes.router)
    dp.include_router(newnote.router)
    dp.include_router(removenote.router)
    dp.include_router(admin.router)
    
    asyncio.create_task(check_reminders(bot))
    try:
        print("Bot is running...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
