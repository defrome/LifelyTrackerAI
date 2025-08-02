from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession


from database.models import DBUser
from keyboard.kb_editor import main_menu_kb, log_indicators_kb

router = Router()

@router.message(Command('start'))
async def send_welcome(message: types.message, session: AsyncSession):
    user = message.from_user
    username = user.username


    db_user = await session.get(DBUser, user.id)

    if not db_user:

        new_user = DBUser(
            id=user.id,
            username=username
        )
        session.add(new_user)
        await session.commit()
    elif db_user.username != username:

        db_user.username = username
        await session.commit()

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


@router.callback_query(F.data == "log_indicators")
async def log_indicators(callback: CallbackQuery):

    await callback.answer()


    await callback.message.edit_text(
        text="Выберите показатель для записи:",
        reply_markup=log_indicators_kb()
    )