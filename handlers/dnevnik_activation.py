from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiosqlite import Connection

from database.dnevnik_account import (
    activate_dnenik,
    deactivate_dnevnik,
    get_account_status,
)
from keyboards.common_menus import start_menu

router = Router()


@router.message(Command("activate"))
@router.callback_query(F.data == "home:activation")
async def cmd_activate_dnevnik(event: Message | CallbackQuery, db: Connection):
    is_message = isinstance(event, Message)
    if await get_account_status(db=db, tg_id=event.from_user.id) == "active":
        await event.answer(
            "У тебя уже <b>активирован</b> аккаунт"
            if is_message
            else "У тебя уже активирован аккаунт"
        )
        return

    await activate_dnenik(db=db, tg_id=event.from_user.id)
    text = "Аккаунт успешно <b>активирован</b> вновь. Теперь ты можешь увидеть свои оценки или сравнить их с оценками других"
    if is_message:
        await event.answer(text, reply_markup=start_menu())
    else:
        await event.message.edit_text(text, reply_markup=start_menu())
        await event.answer()


@router.message(Command("deactivate"))
async def cmd_deactivate_dnevnik(message: Message, db: Connection):
    if await get_account_status(db=db, tg_id=message.from_user.id) == "inactive":
        await message.answer("У тебя уже <b>деактивирован</b> аккаунт")
        return

    await deactivate_dnevnik(db=db, tg_id=message.from_user.id)
    await message.answer(
        "Аккаунт успешно <b>деактивирован</b>. Чтобы снова смотреть свои оценки, просто напиши /activate"
    )
