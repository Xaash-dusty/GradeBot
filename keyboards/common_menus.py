from aiogram.enums import ButtonStyle
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_menu(is_active=True):
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="Профиль", callback_data="home:profile", style=ButtonStyle.PRIMARY
        )
    )
    if is_active:
        builder.add(
            InlineKeyboardButton(
                text="Мои оценки",
                callback_data="home:my_marks",
                style=ButtonStyle.SUCCESS,
            )
        )
        builder.add(
            InlineKeyboardButton(
                text="Что выходит",
                callback_data="home:my_final",
                style=ButtonStyle.SUCCESS,
            )
        )
        builder.add(
            InlineKeyboardButton(
                text="Сравнить c другими",
                callback_data="home:compare",
                style=ButtonStyle.PRIMARY,
            )
        )
    else:
        builder.add(
            InlineKeyboardButton(
                text="Активировать аккаунт",
                callback_data="home:activation",
                style=ButtonStyle.SUCCESS,
            )
        )
    builder.add(
        InlineKeyboardButton(
            text="Оценки всего класса", callback_data="home:general_marks"
        )
    )
    builder.add(
        InlineKeyboardButton(text="Последняя кр/ср", callback_data="home:last_work")
    )

    builder.add(
        InlineKeyboardButton(text="Посмотреть топ", callback_data="home:look_top")
    )

    if is_active:
        builder.adjust(2, 2, 1, 1, 1)
    else:
        builder.adjust(1)

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


def confirm_kb(cb_on_yes: str, cb_on_no: str):
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="Да", callback_data=cb_on_yes, style=ButtonStyle.SUCCESS
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="Нет", callback_data=cb_on_no, style=ButtonStyle.DANGER
        )
    )

    builder.adjust(2)
    return builder.as_markup()
