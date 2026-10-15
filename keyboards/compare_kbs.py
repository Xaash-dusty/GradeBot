from aiogram.enums import ButtonStyle
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def under_personal_subject_kb():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="Сравнить с другими",
            callback_data="compare:subject",
            style=ButtonStyle.PRIMARY,
        )
    )

    builder.add(
        InlineKeyboardButton(
            text="Вернуться назад",
            callback_data="back:my_marks",
            style=ButtonStyle.DANGER,
        )
    )

    builder.adjust(1)
    return builder.as_markup()
