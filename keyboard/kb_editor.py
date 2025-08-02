from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder,
    InlineKeyboardBuilder
)


def main_menu_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="📝 Записать показатели", callback_data="log_indicators")
    builder.button(text="📊 Статистика", callback_data="show_stats")
    builder.button(text="⚙️ Настройки", callback_data="settings")
    builder.button(text="ℹ️ Помощь", callback_data="help")

    builder.adjust(1, 2, 1)  # 2 кнопки в первом ряду, остальные во втором
    return builder.as_markup()

def log_indicators_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Записать прием воды", callback_data="water_ind")
    builder.button(text="Записать прием пищи", callback_data="eat_ind")
    builder.button(text="Записать весовые и ростовые показатели", callback_data="ves_and_rost_ind")
    builder.button(text="Помощь искусственного интелекта", callback_data="ai_help")

    builder.adjust(2, 1, 1)
    return builder.as_markup()