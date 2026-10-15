import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiosqlite import Connection

from database.dnevnik_account import link_dnevnik
from database.user_account import get_person_id_by_password, is_valid_person_id

logger = logging.getLogger(__name__)


class AuthStates(StatesGroup):
    waiting_for_password = State()


router = Router()


@router.message(AuthStates.waiting_for_password, F.text, ~F.text.startswith("/"))
async def on_password(message: Message, state: FSMContext, db: Connection):
    tg_id = message.from_user.id
    password = message.text
    person_id = await get_person_id_by_password(db=db, password=password)

    if person_id is None:
        await message.answer(
            "❌ Неверный пароль. Попробуй еще раз или напиши мне @Xaash_dusty"
        )
        logger.warning(
            f"Пользователь ввел неверный пароль\n{tg_id = }\t{password = }\t{person_id = }"
        )
        return
    # Хоть пароль и есть он может быть занят. Проверяем на всякий случай
    if not await is_valid_person_id(db=db, person_id=person_id):
        await message.answer(
            "Произошла какая-то ошибка. Пользователь с таким паролем уже есть\n\nЗа помощью обратись ко мне @Xaash_dusty"
        )
        logger.error(
            "Пользователь не смог войти с паролем, т.к. аккаунт с тами паролем уже занят\n"
            f"{tg_id = }\t{person_id = }\t{password = }"
        )
        return

    if await link_dnevnik(db=db, tg_id=message.from_user.id, person_id=person_id):
        await message.answer(
            "Дневник успешно привязан, теперь ты можешь отслеживать свои оценки, сравнивать их с оценками одноклассников и многое другое\n\nДля более подробной инструкции /help"
        )
    else:
        await message.answer(
            "Не удалось привязать дневник. За помощью обратись ко мне @Xaash_dusty"
        )
    await state.clear()


@router.message(AuthStates.waiting_for_password)
async def on_invalid_password(message: Message):
    if message.text is not None and message.text.startswith("/"):
        await message.answer(
            "В данный момент комнады недоступны. Сначала ты должен ввести пароль"
        )
        return
    await message.answer("Ты должен ввести 8-значный пароль (текст)")
