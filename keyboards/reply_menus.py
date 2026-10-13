from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_menu_kb():
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Мои оценки", callback_data="my_marks"))
    builder.add(
        InlineKeyboardButton(text="Общие оценки", callback_data="general_marks")
    )
    # Оценки другого ученика только если есть доступ и права
    builder.add(
        InlineKeyboardButton(
            text="Оценки другого ученика", callback_data="person_marks"
        )
    )
    builder.add(InlineKeyboardButton(text="Мой профиль", callback_data="my_profile"))

    builder.adjust(1)
    return builder.as_markup()


def link_account_kb():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="Общие оценки", callback_data="general_marks")
    )
    builder.add(
        InlineKeyboardButton(text="Привязать дневник", callback_data="link_dnevnik")
    )
    builder.add(InlineKeyboardButton(text="Мой профиль", callback_data="my_profile"))

    builder.adjust(1)
    return builder.as_markup()
