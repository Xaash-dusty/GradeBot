import logging
import math

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiosqlite import Connection, Row

from database.dnevnik_account import get_account_status
from database.get_personal_school_data import get_user_marks
from keyboards.personal_marks_kbs import (
    my_marks_all_back_kb,
    my_marks_all_kb,
    my_marks_kb,
)

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("my_marks"))
@router.callback_query(F.data.endswith("my_marks"))
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
@router.callback_query(F.data.endswith("my_marks:all"))
async def cmd_my_marks_all(event: Message | CallbackQuery, db: Connection):
    is_message = isinstance(event, Message)
    if await get_account_status(db=db, tg_id=event.from_user.id) != "active":
        await event.answer("Твой аккаунт не активирован. Для активации /activate")
        return

    rows: list[Row] = await get_user_marks(db=db, tg_id=event.from_user.id)
    blocks: list[str] = []
    for subject, marks, wa_score in rows:
        total = math.floor(float(wa_score) + 0.5)
        blocks.append(
            f"<b>{subject} — {wa_score} — {total}</b>\n<i>Оценки: {marks}</i>"
        )

    text = f"<b>{'Мои оценки':^90}</b>\n\n{'\n\n'.join(blocks)}"
    if is_message:
        await event.answer(text, reply_markup=my_marks_all_kb())
    else:
        await event.message.edit_text(text, reply_markup=my_marks_all_kb())
        await event.answer()


@router.message(Command("my_marks_table"))
@router.callback_query(F.data == "my_marks:all:table")
async def cmd_my_marks_all_table(event: Message | CallbackQuery, db: Connection):
    is_message = isinstance(event, Message)
    if await get_account_status(db=db, tg_id=event.from_user.id) != "active":
        await event.answer("Твой аккаунт не активирован. Для активации /activate")
        return

    rows: list[Row] = await get_user_marks(db=db, tg_id=event.from_user.id)
    max_subject_len: int = max(len(row["subject"]) for row in rows)
    lines: list[str] = [
        f"<b>{'Предмет':<{max_subject_len}} | {'Оценка':<25} | Ср.вз</b>"
    ]

    for r in rows:
        lines.append(
            f"{r['subject']:<{max_subject_len}} | {r['marks']:<25} | {r['wa_score']}"
        )

    text = f"<b>{'Мои оценки'.center(90)}</b>\n\n<pre>{'\n'.join(lines)}</pre>"
    if is_message:
        await event.answer(text, reply_markup=my_marks_all_back_kb())
    else:
        await event.message.edit_text(text, reply_markup=my_marks_all_back_kb())
        await event.answer()


async def get_total_marks(rows: list[Row]) -> list[str]:
    max_subject_len: int = max(len(row["subject"]) for row in rows)
    lines: list[str] = [
        f"<b>{'Предмет':<{max_subject_len}} | {'Ср.вз':^6} | Итог</b>"
    ]
    for r in rows:
        total = math.floor(float(r["wa_score"]) + 0.5)
        lines.append(
            f"{r['subject']:<{max_subject_len}} | {r['wa_score']:^6} | {total}"
        )
    return lines


def get_absolute_score(rows: list[Row]) -> float:
    totals = [math.floor(float(r["wa_score"]) + 0.5) for r in rows]
    return sum(totals) / len(totals)


def get_count_marks(rows: list[Row]) -> dict[str, int]:
    pass


@router.message(Command("my_final"))
@router.callback_query(F.data.endswith("my_final"))
async def cmd_personal_final(event: Message | CallbackQuery, db: Connection):
    """Что тут писать?
    1 Краткий список: предмет - ср.вз - итог балл
    2 Итоговый средний балл за все предметы
    3 Сколько каких оценок
    4 По каким предметам спорные баллы например 4,5 +-0,25 или по каким предметам не хватает 1 оценки для повышения балла
    Для таких предметов показывать сколько уроков осталось
    Как реализовать?
    Функция get_user_marks возвращает нужные значения. Сделать функции прогрозов и аналитики
    """
    is_message = isinstance(event, Message)
    if await get_account_status(db=db, tg_id=event.from_user.id) != "active":
        await event.answer("Твой аккаунт не активирован. Для активации /activate")
        return

    raw_marks: list[Row] = await get_user_marks(db=db, tg_id=event.from_user.id)
    results: list[str] = []

    total_marks = f"<pre>{'\n'.join(await get_total_marks(raw_marks))}</pre>"
    results.append(total_marks)

    absolute_score = f"Общий средний балл {get_absolute_score(raw_marks)}"
    results.append(absolute_score)

    # count_marks = get_count_marks(raw_marks)
    # results.append(count_marks)
    if is_message:
        await event.answer("\n\n\n".join(results))
    else:
        await event.message.edit_text("\n\n\n".join(results))
        await event.answer()
