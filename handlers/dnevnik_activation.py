from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiosqlite import Connection

from database.dnevnik_relations import (
    activate_dnenik,
    deactivate_dnevnik,
    get_account_status,
)
from keyboards.common_menus import active_account_start_menu

router = Router()


@router.message(Command("activate"))
async def cmd_activate_dnevnik(message: Message, db: Connection):
    account_status = await get_account_status(db=db, tg_id=message.from_user.id)
    if account_status == "active":
        await message.answer("У тебя уже привязан дневник")
    elif account_status == "None":
        await message.answer(
            "Ты еще никогда не привязывал дневник. Для привязки дневника /link"
        )
    else:
        await activate_dnenik(db=db, tg_id=message.from_user.id)
        await message.answer(
            "Дневник успешно привязан вновь. Теперь ты можешь увидеть свои оценки или сравнить их с оценками других",
            reply_markup=active_account_start_menu()
        )


@router.message(Command("deactivate"))
async def cmd_deactivate_dnevnik(message: Message, db: Connection):
    account_status = await get_account_status(db=db, tg_id=message.from_user.id)
    if account_status == "None":
        await message.answer("У тебя не привязан дневник. Для привязки дневника /link")
        return
    elif account_status == "inactive":
        await message.answer("Дневник уже отвязан")
    else:
        await deactivate_dnevnik(db=db, tg_id=message.from_user.id)
        await message.answer(
            "Дневник успешно отвязан. Чтобы снова смотреть свои оценки, просто напиши /activate"
        )
