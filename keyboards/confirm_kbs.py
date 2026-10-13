from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def yes_or_no_kb(cb_on_yes: str, cb_on_no: str):
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Да", callback_data=cb_on_yes))
    builder.add(InlineKeyboardButton(text="Нет", callback_data=cb_on_no))

    builder.adjust(2)
    return builder.as_markup()