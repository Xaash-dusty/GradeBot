from aiogram import Router
from aiogram.enums import ButtonStyle
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from keyboards.reply_menus import start_menu_kb

router = Router()


@router.message(CommandStart(), StateFilter(None))
async def cmd_start(message: Message):
    await message.answer(
        "Бот запущен\nТеперь ты можешь начать отслеживать свои оценки и пользоваться ботом по максимуму\nДля вызова справки /help",
        reply_markup=start_menu_kb(),
    )


@router.message(Command("help"), StateFilter(None))
async def cmd_help(message: Message):
    text = "Инструкция по использованию бота"
    await message.answer(text)


@router.message(Command("test"), StateFilter(None))
async def test(m: Message):
    text = "<b>Какой-то</b> <code>текст</code>"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📚 Оценки", callback_data="marks", style=ButtonStyle.PRIMARY
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Сохранить", callback_data="save", style=ButtonStyle.SUCCESS
                ),
                InlineKeyboardButton(
                    text="🗑 Удалить", callback_data="delete", style=ButtonStyle.DANGER
                ),
            ],
        ]
    )
    await m.answer(text, parse_mode="HTML", reply_markup=keyboard)
