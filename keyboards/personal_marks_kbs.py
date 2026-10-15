from aiogram.enums import ButtonStyle
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def my_marks_kb():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="Все оценки", callback_data="my_marks:all", style=ButtonStyle.SUCCESS
        )
    )
    builder.add(
        InlineKeyboardButton(text="Статистика", callback_data="my_marks:statistics")
    )

    builder.add(
        InlineKeyboardButton(
            text="Последние оценки и работы",
            callback_data="my_marks:latest",
        )
    )

    builder.add(
        InlineKeyboardButton(
            text="Оценки по предмету",
            callback_data="my_marks:subject",
            style=ButtonStyle.PRIMARY,
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="Назад", callback_data="back:home", style=ButtonStyle.DANGER
        )
    )

    builder.adjust(2, 1, 1, 1)
    return builder.as_markup()


def my_marks_back_kb():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="Назад", callback_data="back:my_marks", style=ButtonStyle.DANGER
        )
    )

    builder.adjust(1)
    return builder.as_markup()


def my_marks_all_kb():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="Получить в виде таблицы",
            callback_data="my_marks:all:table",
            style=ButtonStyle.PRIMARY,
        )
    )

    builder.add(
        InlineKeyboardButton(
            text="Назад", callback_data="back:my_marks", style=ButtonStyle.DANGER
        )
    )

    builder.adjust(1)
    return builder.as_markup()


def my_marks_all_back_kb():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="Назад", callback_data="back:my_marks:all", style=ButtonStyle.DANGER
        )
    )

    builder.adjust(1)
    return builder.as_markup()


def my_marks_latest_kb():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="Оценки за неделю", callback_data="my_marks:week")
    )
    builder.add(
        InlineKeyboardButton(
            text="Оценки за сегодня",
            callback_data="my_marks:today",
            style=ButtonStyle.PRIMARY,
        )
    )

    builder.add(
        InlineKeyboardButton(
            text="Последние кр/ср", callback_data="my_marks:latest_works"
        )
    )

    builder.add(
        InlineKeyboardButton(
            text="Назад", callback_data="back:my_marks", style=ButtonStyle.DANGER
        )
    )

    builder.adjust(2, 1, 1)
    return builder.as_markup()


def my_marks_subject_kb(subjects):
    builder = ReplyKeyboardBuilder()

    for subject in subjects:
        builder.button(text=subject["subject"])

    builder.adjust(4)
    return builder.as_markup(
        resize_keyboard=True, input_field_placeholder="Пример: Алгебра"
    )
