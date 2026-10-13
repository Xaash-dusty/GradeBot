import logging

from aiosqlite import Connection

logger = logging.getLogger(__name__)


async def get_role(db: Connection, tg_id: int) -> str:
    async with db.execute(
        "SELECT role FROM user_roles WHERE telegram_id = ?", (tg_id,)
    ) as cursor:
        row = await cursor.fetchone()
        return row["role"]


async def is_banned(db: Connection, tg_id: int) -> bool:
    async with db.execute(
        "SELECT 1 FROM bans WHERE telegram_id = ? LIMIT 1", (tg_id,)
    ) as cursor:
        return await cursor.fetchone() is not None
