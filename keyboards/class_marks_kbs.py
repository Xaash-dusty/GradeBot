from aiogram.enums import ButtonStyle
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def general_marks_kb():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="Ср баллы по предметам", callback_data="general_marks:avgs"
        )
    )
    # Возможно удобно добавить reply клавиатуру со всеми предметами
    builder.add(
        InlineKeyboardButton(
            text="Оценки по 1 предмету",
            callback_data="general_marks:subject",
            style=ButtonStyle.PRIMARY,
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="Последняя кр/ср", callback_data="general_marks:last_work"
        )
    )

    builder.add(
        InlineKeyboardButton(
            text="Назад", callback_data="back:home", style=ButtonStyle.DANGER
        )
    )

    builder.adjust(1, 2, 1)
    return builder.as_markup()


def general_marks_back_kb():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="Назад", callback_data="back:general_marks", style=ButtonStyle.DANGER
        )
    )

    builder.adjust(1)
    return builder.as_markup()
