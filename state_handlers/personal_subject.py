import logging
from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiosqlite import Connection, Row

from database.dnevnik_account import get_account_status
from database.get_class_school_data import get_subjects
from database.get_personal_school_data import get_subject_id, get_user_subject_marks
from keyboards.compare_kbs import under_personal_subject_kb
from keyboards.personal_marks_kbs import my_marks_kb, my_marks_subject_kb

router = Router()
logger = logging.getLogger(__name__)


class SubjectState(StatesGroup):
    waiting_for_subject = State()


@router.message(Command("cancel"), StateFilter(SubjectState))
async def cancel_form(message: Message, state: FSMContext):
    await message.answer(
        "Выбор предмета <b>отменен</b>", reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        "Выбери, что еще ты хотел бы узнать", reply_markup=my_marks_kb()
    )
    await state.clear()


@router.message(Command("my_marks_subject"), StateFilter(None))
@router.callback_query(F.data == "my_marks:subject", StateFilter(None))
async def cmd_my_marks_subject(
    event: Message | CallbackQuery, db: Connection, state: FSMContext
):
    is_message = isinstance(event, Message)
    if await get_account_status(db=db, tg_id=event.from_user.id) != "active":
        await event.answer(
            "Твой аккаунт <b>не активирован</b>. Для активации /activate"
            if is_message
            else "Твой аккаунт не активирован"
        )
        return

    subjects = await get_subjects(db=db)
    if is_message:
        await event.answer(
            "Напиши название предмета, оценки которого ты хочешь получить или воспользуйся клавиатурой\n\nДля отмены /cancel",
            reply_markup=my_marks_subject_kb(subjects),
        )
    else:
        await event.message.delete()
        await event.message.answer(
            "Напиши название предмета, оценки которого ты хочешь получить или воспользуйся клавиатурой\n\nДля отмены /cancel",
            reply_markup=my_marks_subject_kb(subjects),
        )
        await event.answer()

    await state.set_state(SubjectState.waiting_for_subject)


@router.message(SubjectState.waiting_for_subject, F.text, ~F.text.startswith("/"))
async def on_subject(message: Message, state: FSMContext, db: Connection):
    if await get_account_status(db=db, tg_id=message.from_user.id) != "active":
        await message.answer(
            "Твой аккаунт <b>не активирован</b>. Для активации /activate"
        )
        return

    subject_id: int | None = await get_subject_id(db=db, subject=message.text)
    if subject_id is None:
        await message.answer(
            "Такого предмета нет. Выбери корректный предмет, используя клавиатуру, или отмени /cancel"
        )
        return

    await state.clear()

    rows: list[Row] = await get_user_subject_marks(
        db=db, tg_id=message.from_user.id, subject_id=subject_id
    )
    blocks: list[str] = []
    for r in rows:
        date = datetime.fromisoformat(r["date"]).strftime("%d.%m")
        blocks.append(
            f"📊 <b>Оценка: {r['mark']}</b> (вес: {r['weight']}) | 🗓 {date}\n"
            f"└ <i>Тип:</i> {r['type']}\n"
            f"└ <i>Тема:</i> {r['title']}"
        )

    text = f"<b>{message.text.upper():^90}</b>\n\n{'\n\n'.join(blocks)}"
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await message.answer(
        f"Ты можешь сравнить свои оценки по предмету '{message.text}' с другими учениками",
        reply_markup=under_personal_subject_kb(),
    )


@router.message(SubjectState.waiting_for_subject)
async def on_invalid_subject(message: Message):
    if message.text is not None and message.text.startswith("/"):
        await message.answer(
            "В данный момент комнады недоступны. Чтобы прекратить выбор предмета напиши /cancel"
        )
        return
    await message.answer(
        "Ты должен ввести имя предмета. Воспользуйся клавиатурой или отмени /cancel"
    )
