from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiosqlite import Connection

from database.dnevnik_relations import (
    activate_dnenik,
    deactivate_dnevnik,
    has_any_account,
    is_active_account,
    is_valid_person_id,
    link_dnevnik,
)
from keyboards.confirm_kbs import yes_or_no_kb

router = Router()


class RemoteDnevnik(StatesGroup):
    person_id = State()


@router.message(Command("cancel"), StateFilter(RemoteDnevnik))
async def cancel_linking(message: Message, state: FSMContext):
    await message.answer("Привязывание дневника отменено")
    await state.clear()


@router.message(Command("linkdnevnik"), StateFilter(None))
@router.callback_query(F.data == "link_dnevnik", StateFilter(None))
async def cmd_link_dnevnik(
    event: Message | CallbackQuery, state: FSMContext, db: Connection
):
    has_account = await has_any_account(db=db, tg_id=event.from_user.id)
    if has_account:
        is_active = await is_active_account(db=db, tg_id=event.from_user.id)
        if is_active:
            await event.answer("У тебя уже привязан дневник")
        else:
            await event.answer(
                "Ты уже привязывал дневник. Хочешь восстановить его?",
                reply_markup=yes_or_no_kb(
                    cb_on_yes="restore_dnevnik", cb_on_no="non-restore_dnevnik"
                ),
            )
        return

    await state.set_state(RemoteDnevnik.person_id)
    if isinstance(event, Message):
        await event.answer("Напиши свой id дневника")
    else:
        await event.message.edit_text("Напиши свой id дневника")
        await event.answer()


@router.callback_query(F.data == "restore_dnevnik")
async def cb_restore_dnevnik(callback: CallbackQuery, db: Connection):
    await activate_dnenik(db=db, tg_id=callback.from_user.id)
    await callback.message.edit_text("Дневник вновь привязан")
    await callback.answer()


@router.callback_query(F.data == "non-restore_dnevnik")
async def cb_non_restore_dnevnik(callback: CallbackQuery):
    await callback.message.edit_text("Ну, не хочешь как хочешь")
    await callback.answer()


@router.message(StateFilter(RemoteDnevnik.person_id), F.text, ~F.text.startswith("/"))
async def on_person_id(message: Message, state: FSMContext, db: Connection):
    if not message.text.isdigit():
        await message.answer("Введите число")
        return

    is_valid = await is_valid_person_id(db=db, person_id=message.text)
    if not is_valid:
        await message.answer(
            "Такого id нету или он уже занят. Введите корректный id дневника"
        )
        return

    is_success = await link_dnevnik(
        db=db, tg_id=message.from_user.id, person_id=int(message.text)
    )
    if is_success:
        await message.answer("Дневник привязан")
    else:
        await message.answer(
            "Не удалось привязать дневник, за помощью обращаться к @Xaash_dusty"
        )
    await state.clear()


@router.message(StateFilter(RemoteDnevnik.person_id))
async def on_invalid_person_id(message: Message):
    if message.text is not None and message.text.startswith("/"):
        await message.answer(
            "В данный момент комнады недоступны. Чтобы прекратить привязку дневника напишите /cancel"
        )
        return
    await message.answer("Вы должны ввести число")


@router.message(Command("deactivatednevnik"))
async def cmd_unlink_dnevnik(message: Message, db: Connection):
    if not await has_any_account(db=db, tg_id=message.from_user.id):
        await message.answer("У вас не привязан дневник")
        return

    await deactivate_dnevnik(db=db, tg_id=message.from_user.id)
    await message.answer("Дневник отвязан")
