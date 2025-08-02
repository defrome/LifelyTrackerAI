from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import requests
import asyncio

from keyboard.kb_editor import main_menu_kb

BOT_TOKEN='8124788304:AAGbT5IlXTC15WeuMz-1f2PgHeCq1oo5tEw'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def send_welcome(message: types.message):
    username = message.from_user.username
    await message.reply(f"""
👋 Привет, @{username}!

Я - твой персональный помощник для отслеживания здоровья. Со мной ты сможешь:

• 📝 Записывать важные показатели (давление, пульс, температуру)
• 📊 Анализировать статистику и прогресс
• ⏰ Получать напоминания о приёме лекарств
• 🏆 Формировать полезные привычки

Давай начнём заботиться о твоём здоровье вместе! 

Выбери действие в меню ниже 👇
    """, reply_markup=main_menu_kb())



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())