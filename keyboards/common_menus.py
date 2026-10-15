from aiogram.enums import ButtonStyle
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def inactive_account_start_menu():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="Профиль", callback_data="home:profile", style=ButtonStyle.PRIMARY
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="Активировать аккаунт",
            callback_data="home:activation",
            style=ButtonStyle.SUCCESS,
        )
    )

    builder.add(
        InlineKeyboardButton(
            text="Оценки по классу", callback_data="home:general_marks"
        )
    )
    builder.add(
        InlineKeyboardButton(text="Последняя кр/ср", callback_data="home:last_work")
    )

    builder.add(
        InlineKeyboardButton(text="Посмотреть топ", callback_data="home:look_top")
    )

    builder.adjust(2, 2, 1)
    return builder.as_markup()


def active_account_start_menu():
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Профиль", callback_data="home:profile", style=ButtonStyle.PRIMARY))
    builder.add(
        InlineKeyboardButton(
            text="Мои оценки", callback_data="home:my_marks", style=ButtonStyle.SUCCESS
        )
    )

    builder.add(
        InlineKeyboardButton(
            text="Оценки по классу", callback_data="home:general_marks"
        )
    )
    builder.add(
        InlineKeyboardButton(text="Последняя кр/ср", callback_data="home:last_work")
    )

    builder.add(
        InlineKeyboardButton(text="Посмотреть топ", callback_data="home:look_top")
    )
    builder.add(
        InlineKeyboardButton(
            text="Сравнить c другими", callback_data="home:compare_marks", style=ButtonStyle.PRIMARY
        )
    )

    builder.adjust(2, 2, 2)
    return builder.as_markup()


def back_home_kb():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="Назад", callback_data="back:home", style=ButtonStyle.DANGER
        )
    )

    builder.adjust(1)
    return builder.as_markup()
