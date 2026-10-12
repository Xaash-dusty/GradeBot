import aiosqlite
from aiogram import Router
from aiogram.enums import ButtonStyle
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from database.telegram_users import add_user

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, db: aiosqlite.Connection):
    await message.answer(
        "Бот запущен\nТеперь ты можешь начать отслеживать свои оценки и пользоваться ботом по максимуму\nДля вызова справки /help"
    )
    await add_user(
        db=db,
        tg_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    text = "Инструкция по использованию бота"
    await message.answer(text)


@router.message(Command("test"))
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
