from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
import requests
import asyncio

from database.db import lifespan
from handlers.handlers import router
from keyboard.kb_editor import main_menu_kb, log_indicators_kb

BOT_TOKEN='8124788304:AAGbT5IlXTC15WeuMz-1f2PgHeCq1oo5tEw'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(lifespan=lifespan)  # Передаем lifespan

    # Регистрируем роутеры
    from handlers import handlers
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())