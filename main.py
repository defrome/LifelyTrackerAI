from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import requests
import asyncio

BOT_TOKEN='8124788304:AAGbT5IlXTC15WeuMz-1f2PgHeCq1oo5tEw'
API_URL='https://trychatgpt.ru/chat/688dedc44172f1f651595753'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def send_welcome(message: types.message):
    await message.reply("Привет отправь мне запрос.")


@dp.message()
async def handle_query(message: types.Message):
    user_query = message.text

    try:
        # Отправляем запрос на сайт (API)
        response = requests.get(f"{API_URL}?query={user_query}")
        data = response.json()  # Если ответ в JSON

        # Отправляем ответ пользователю
        await message.reply(f"Ответ с сайта:\n{data['result']}")  # Замените data['result'] на нужное поле из ответа

    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())