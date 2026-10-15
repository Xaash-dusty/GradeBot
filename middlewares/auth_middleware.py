from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, TelegramObject
from aiosqlite import Connection

from database.dnevnik_relations import get_account_status
from handlers.check_password import AuthStates


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not event.from_user:
            return await handler(event, data)

        db: Connection = data.get("db")
        state: FSMContext = data.get("state")
        current_state = await state.get_state()

        # Если пользователь уже находится в процессе ввода пароля — разрешаем ему писать
        if current_state == AuthStates.waiting_for_password.state:
            return await handler(event, data)

        # Проверяем статус аккаунта
        account_status = await get_account_status(db=db, tg_id=event.from_user.id)

        if account_status == "None":
            # Включаем состояние ожидания пароля
            await state.set_state(AuthStates.waiting_for_password)

            # Отвечаем в зависимости от типа события
            if isinstance(event, Message):
                await event.answer(
                    "У тебя нет аккаунта. Чтобы получить доступ к боту\n"
                    "Введи пароль...\n\n"
                    "Если у тебя нет пароля, обратись ко мне @Xaash_dusty"
                )
            elif isinstance(event, CallbackQuery):
                await event.answer(
                    "Доступ ограничен. Введи пароль в чате.", show_alert=True
                )

            return  # Прерываем выполнение, к хэндлерам событие не идет

        return await handler(event, data)
