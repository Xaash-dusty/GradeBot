from aiogram import F, Router
from aiogram.types import Message

router = Router()


@router.message(F.text)
async def on_unknown_msg(message: Message):
    if message.text == "/cancel":
        await message.answer("Нельзя использовать отмену вне формы")
    elif message.text.startswith("/"):
        await message.answer(f"Команда '{message.text}' не найдена\n\nДля вызова инструкций /help")
    else:
        await message.answer(
            "Я не умею общаться. Что ты от меня хочешь\n\nДля вызова инструкций /help"
        )


@router.message()
async def handle_all(message: Message):
    await message.answer(
        "Понятия не имею, что это значит\n\nДля вызова инструкций /help"
    )