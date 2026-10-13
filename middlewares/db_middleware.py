from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiosqlite import Connection

from database.user_management import add_user
from database.verifications import is_banned


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, db: Connection):
        self.db = db
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data["db"] = self.db

        await add_user(
            db=self.db,
            tg_id=event.from_user.id,
            first_name=event.from_user.first_name,
            username=event.from_user.username,
        )

        in_ban = await is_banned(db=self.db, tg_id=event.from_user.id)
        
        if not in_ban:
            return await handler(event, data)
        else:
            await event.answer("Вы забанены")
