from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

router = Router()


@router.message(F.text)
async def on_unknown_msg(message: Message):
    if message.text == "/cancel":
        await message.answer("Нельзя использовать отмену вне формы")
    elif message.text.startswith("/"):
        await message.answer(
            f"Команда '{message.text}' не найдена\n\nДля вызова инструкций /help"
        )
    else:
        await message.answer(
            "Я не умею общаться. Чего ты от меня хочешь\n\nДля вызова инструкций /help"
        )


@router.message()
@router.callback_query()
async def handle_all(event: Message | CallbackQuery):
    if isinstance(event, Message):
        await event.answer(
            "Понятия не имею, что это значит\n\nДля вызова инструкций /help"
        )
    else:
        await event.answer(f"Я не знаю что делать с колбэком {event.data}")