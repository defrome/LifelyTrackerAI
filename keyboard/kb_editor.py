from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder,
    InlineKeyboardBuilder
)

def main_menu_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text="📝 Записать показатели")
    builder.button(text="📊 Статистика")
    builder.button(text="⚙️ Настройки")
    builder.button(text="ℹ️ Помощь")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)