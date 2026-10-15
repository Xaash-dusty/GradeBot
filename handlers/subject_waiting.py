from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiosqlite import Connection

from database.dnevnik_relations import get_account_status
from database.get_other_school_data import get_subjects
from keyboards.my_marks_kbs import my_marks_subject_kb, my_marks_back_kb

router = Router()


class SubjectState(StatesGroup):
    waiting_subject = State()


@router.message(Command("cancel"), StateFilter(SubjectState))
async def cancel_form(message: Message, state: FSMContext):
    await message.answer("Форма отменена")
    await state.clear()


@router.message(Command("my_marks_subject"), StateFilter(None))
@router.callback_query(F.data == "my_marks:subject", StateFilter(None))
async def cmd_my_marks_subject(
    event: Message | CallbackQuery, db: Connection, state: FSMContext
):
    is_message = isinstance(event, Message)
    if await get_account_status(db=db, tg_id=event.from_user.id) != "active":
        await event.answer("Твой аккаунт не активирован. Для активации /activate")
        return

    await state.set_state(SubjectState.waiting_subject)
    subjects = await get_subjects(db=db)
    # Сначала протестит как выглядит reply клава
    if is_message:
        # Прикрепить 2 клавиатуры по 1 к каждому сообщению
        await event.answer(
            "Теперь тебе необходимо написать название предмета. Можешь воспользоваться клавиатурой\nДля отмены выбора предмета /cancel",
            reply_markup=my_marks_subject_kb(subjects),
        )
        await event.answer("Введи название предмета, например: Физика", reply_markup=my_marks_back_kb())
    else:
        # Прикрепить 2 клавиатуры по 1 к каждому сообщению
        await event.message.answer(
            "Теперь тебе необходимо написать название предмета. Можешь воспользоваться клавиатурой\nДля отмены выбора предмета /cancel",
            reply_markup=my_marks_subject_kb(subjects),
        )
        await event.message.answer("Введи название предмета, например: Физика")
        await event.answer()


@router.message(
    StateFilter(SubjectState.waiting_subject), F.text, ~F.text.startswith("/")
)
async def on_subject(message: Message, state: FSMContext, db: Connection):
    pass


@router.message(StateFilter(SubjectState.waiting_subject))
async def on_invalid_subject(message: Message):
    if message.text is not None and message.text.startswith("/"):
        await message.answer(
            "В данный момент комнады недоступны. Чтобы прекратить выбор предмета напиши /cancel"
        )
        return
    await message.answer("Ты должен ввести имя предмета. Воспользуйся клавиатурой")
