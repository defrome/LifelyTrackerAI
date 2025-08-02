import numpy as np
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.ext.asyncio import AsyncSession

from ai.ai_main import questions, answers
from database.models import DBUser
from keyboard.kb_editor import main_menu_kb, log_indicators_kb, ai_back_kb

router = Router()


@router.message(Command('start'))
async def send_welcome(message: types. Message, session: AsyncSession):
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


vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(questions)


def get_answer(user_question: str) -> str:
    try:
        user_vector = vectorizer.transform([user_question])
        similarities = cosine_similarity(user_vector, question_vectors)
        most_similar_idx = np.argmax(similarities)
        similarity_score = similarities[0, most_similar_idx]

        if similarity_score > 0.5:
            return answers[most_similar_idx]
        return "Не нашел точного ответа. Попробуйте переформулировать вопрос."
    except Exception as e:
        return f"Ошибка обработки вопроса: {str(e)}"


@router.callback_query(F.data == "ai_help")
async def ai_help_callback(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🤖 Задайте любой вопрос о потреблении воды:\n"
        "Примеры:\n"
        "- Сколько воды нужно пить в день?\n"
        "- Как рассчитать норму по весу?\n"
        "- Нужно ли больше воды при тренировках?",
        reply_markup=ai_back_kb()
    )
    await callback.answer()


@router.message()
async def handle_all_questions(message: types.Message):
    if message.text.startswith('/'):
        return

    answer = get_answer(message.text)
    await message.answer(answer)


@router.callback_query(F.data == "log_indicators")
async def log_indicators(callback: CallbackQuery):

    await callback.answer()


    await callback.message.edit_text(
        text="Выберите показатель для записи:",
        reply_markup=log_indicators_kb()
    )


@router.callback_query(F.data == "back_to_main")
async def back_to_main_handler(callback: CallbackQuery, session: AsyncSession):
    user = callback.from_user
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

    try:

        await callback.message.edit_text(
            text=f"""
👋 Привет, @{username}!

Я - твой персональный помощник для отслеживания здоровья. Со мной ты сможешь:

• 📝 Записывать важные показатели (давление, пульс, температуру)
• 📊 Анализировать статистику и прогресс
• ⏰ Получать напоминания о приёме лекарств
• 🏆 Формировать полезные привычки

Давай начнём заботиться о твоём здоровье вместе! 

Выбери действие в меню ниже 👇
            """,
            reply_markup=main_menu_kb()
        )
    except:
        await callback.message.answer(
            text=f"👋 Главное меню",
            reply_markup=main_menu_kb()
        )

    await callback.answer()