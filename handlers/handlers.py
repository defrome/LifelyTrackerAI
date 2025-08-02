import numpy as np
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.ext.asyncio import AsyncSession

from ai.ai_main import questions, answers
from database.models import DBUser
from keyboard.kb_editor import main_menu_kb, log_indicators_kb, ai_back_kb, back_kb, ai_answ_back_kb

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


class UserData(StatesGroup):
    waiting_for_height = State()
    waiting_for_weight = State()


@router.callback_query(F.data == "ves_and_rost_ind")
async def start_indicators_input(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("📏 Введите ваш рост в сантиметрах:")
    await state.set_state(UserData.waiting_for_height)
    await callback.answer()


@router.message(UserData.waiting_for_height)
async def process_height(message: Message, state: FSMContext):
    try:
        height = int(message.text)
        if not (100 <= height <= 250):
            raise ValueError
        await state.update_data(height=height)
        await message.answer("⚖️ Теперь введите ваш вес в килограммах:")
        await state.set_state(UserData.waiting_for_weight)
    except ValueError:
        await message.answer("❌ Пожалуйста, введите корректный рост (число от 100 до 250 см).")


@router.message(UserData.waiting_for_weight)
async def process_weight(message: Message, state: FSMContext, session: AsyncSession):
    try:
        weight = int(message.text)
        if not (30 <= weight <= 300):
            raise ValueError

        data = await state.get_data()
        height = data['height']


        user = await session.get(DBUser, message.from_user.id)
        if not user:
            user = DBUser(
                id=message.from_user.id,
                username=message.from_user.username,
                height=height,
                weight=weight
            )
            session.add(user)
        else:
            user.height = height
            user.weight = weight

        await session.commit()

        water_norm = round(weight * 0.03, 1)  # 30 мл на 1 кг

        await message.answer(
            f"✅ Данные сохранены!\n\n"
            f"📏 Ваш рост: {height} см\n"
            f"⚖️ Ваш вес: {weight} кг\n"
            f"💧 Рекомендуемая норма воды: {water_norm} л/день\n\n"
            f"Вы можете обновить данные в любое время.",
            reply_markup=back_kb()
        )
        await state.clear()

    except ValueError:
        await message.answer("❌ Пожалуйста, введите корректный вес (число от 30 до 300 кг).")


def calculate_bmi(weight: float, height: float) -> float:
    return weight / ((height / 100) ** 2)

def calculate_waternorm(weight: float, height: float) -> float:
    return weight * 0.03

def calculate_ideal_weight(height: float) -> float:
    return (height - 100) - ((height - 150) / 4)

def get_bmi_status(bmi: float) -> str:
    if bmi < 18.5:
        return "Недостаточный вес"
    elif 18.5 <= bmi < 25:
        return "Нормальный вес"
    elif 25 <= bmi < 30:
        return "Избыточный вес"
    else:
        return "Ожирение"



@router.callback_query(F.data == 'show_stats_profile')
async def show_stats_profile(callback: CallbackQuery, session: AsyncSession):

    user = await session.get(DBUser, callback.from_user.id)

    if user is None or user.height is None or user.weight is None:
        await callback.message.edit_text(
            text="📊 Ваша статистика недоступна\n\n"
                 "Для отображения статистики необходимо ввести ваш рост и вес",
            reply_markup=InlineKeyboardBuilder()
            .button(text="📏 Ввести данные", callback_data="ves_and_rost_ind")
            .button(text="🔙 Назад", callback_data="back_to_main")
            .adjust(1)
            .as_markup()
        )
        return

    bmi = calculate_bmi(user.weight, user.height)
    water_norm = calculate_waternorm(user.weight, user.height)
    ideal_weight = calculate_ideal_weight(user.height)
    bmi_status = get_bmi_status(bmi)

    message_text = (
        f"📊 Ваша персональная статистика\n\n"
        f"📏 Рост: {user.height} см\n"
        f"⚖️ Вес: {user.weight} кг\n"
        f"🧮 ИМТ: {bmi:.1f} ({get_bmi_status(bmi)})\n"
        f"💧 Норма воды: {water_norm:.1f} л/день\n"
        f"🎯 Идеальный вес: {ideal_weight:.1f} кг\n\n"
    )

    kb = InlineKeyboardBuilder()
    kb.button(text="🔄 Обновить данные", callback_data="ves_and_rost_ind")
    kb.button(text="🔙 Назад", callback_data="back_to_main")
    kb.adjust(1)


    await callback.message.edit_text(
        text=message_text,
        reply_markup=kb.as_markup()
    )



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