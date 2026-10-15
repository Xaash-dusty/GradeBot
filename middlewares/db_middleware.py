from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiosqlite import Connection

from database.user_account import add_user, is_banned


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
        if not event.from_user:
            return await handler(event, data)

        data["db"] = self.db

        await add_user(
            db=self.db,
            tg_id=event.from_user.id,
            first_name=event.from_user.first_name,
            username=event.from_user.username,
        )

        in_ban = await is_banned(db=self.db, tg_id=event.from_user.id)

        if in_ban:
            await event.answer("Вы забанены", show_alert=True)
            return
        
        return await handler(event, data)
