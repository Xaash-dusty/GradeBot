import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiosqlite import Connection, Row

from database.dnevnik_relations import get_account_status
from database.get_own_school_data import get_user_marks
from keyboards.my_marks_kbs import my_marks_back_kb, my_marks_kb

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("my_marks"))
@router.callback_query(F.data.endswith(":my_marks"))
async def cmd_my_marks(event: Message | CallbackQuery, db: Connection):
    is_message = isinstance(event, Message)
    if await get_account_status(db=db, tg_id=event.from_user.id) != "active":
        await event.answer("Твой аккаунт не активирован. Для активации /activate")
        return
    # Можно наполнить сообщение объяснениями каждой кнопки каждого действия
    text = f"<b>{'Мои оценки':^90}</b>\n\nВыбери, что ты хочешь узнать"
    if is_message:
        await event.answer(text, reply_markup=my_marks_kb())
    else:
        await event.message.edit_text(text, reply_markup=my_marks_kb())
        await event.answer()


@router.message(Command("my_marks_all"))
@router.callback_query(F.data == "my_marks:all")
async def cmd_my_marks_all(event: Message | CallbackQuery, db: Connection):
    is_message = isinstance(event, Message)
    if await get_account_status(db=db, tg_id=event.from_user.id) != "active":
        await event.answer("Твой аккаунт не активирован. Для активации /activate")
        return

    rows: list[Row] = await get_user_marks(db=db, tg_id=event.from_user.id)
    max_subject_len: int = max(len(row["subject"]) for row in rows)
    lines: list = [f"<b>{'Предмет':<{max_subject_len}} | {'Оценка':<25} | Ср.вз</b>\n"]

    for subject, marks, wa_score in rows:
        subject_fixed: str = subject.ljust(max_subject_len)
        marks_fixed: str = marks.ljust(25)
        lines.append(f"{subject_fixed} | {marks_fixed} | {wa_score}")

    text = f"<b>{'Мои оценки'.center(90)}</b>\n\n<pre>{'\n'.join(lines)}</pre>"
    if is_message:
        await event.answer(text, reply_markup=my_marks_back_kb())
    else:
        await event.message.edit_text(text, reply_markup=my_marks_back_kb())
        await event.answer()
