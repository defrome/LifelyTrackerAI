from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder,
    InlineKeyboardBuilder
)


def main_menu_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="📝 Записать показатели",
        callback_data="log_indicators"
    )
    builder.button(text="📊 Статистика и профиль",
                   callback_data="show_stats_profile"
    )
    builder.button(text="⚙️ Настройки",
                   callback_data="settings"
    )
    builder.button(text="ℹ️ Помощь",
                   callback_data="help"
    )


    builder.adjust(1, 2, 1)
    return builder.as_markup()


from aiogram.utils.keyboard import InlineKeyboardBuilder


def ai_back_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="⬅️ Назад",
        callback_data="log_indicators"
    )

    builder.adjust(1, 1, 1, 2)

    return builder.as_markup()


def back_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="⬅️ Назад",
        callback_data="back_to_main"
    )


    return builder.as_markup()


def log_indicators_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="💧 Записать приём воды",
        callback_data="water_ind"
    )
    builder.button(
        text="🍎 Записать приём пищи",
        callback_data="eat_ind"
    )
    builder.button(
        text="⚖️ Записать вес и рост",
        callback_data="ves_and_rost_ind"
    )
    builder.button(
        text="🤖 Помощь ИИ",
        callback_data="ai_help"
    )
    builder.button(
        text="⬅️ Назад",
        callback_data="back_to_main"
    )

    builder.adjust(1, 1, 1, 2)

    return builder.as_markup()