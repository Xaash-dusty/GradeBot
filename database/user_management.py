import logging

from aiosqlite import Connection

logger = logging.getLogger(__name__)


async def add_user(
    db: Connection,
    tg_id: int,
    first_name: str,
    username: str | None = None,
) -> None:
    query = """INSERT INTO users (telegram_id, username, first_name) VALUES (?, ?, ?)
        ON CONFLICT DO UPDATE SET username = excluded.username, first_name = excluded.first_name, last_activity = datetime("now")
        RETURNING id, last_activity, registration_date"""
    async with db.execute(query, (tg_id, username, first_name)) as cursor:
        row = await cursor.fetchone()
        if row["registration_date"] == row["last_activity"]:
            id_ = row["id"]
            logger.info(f"New user\n{username = }\n{first_name = }\n{id_ = }")

    await db.execute(
        "INSERT OR IGNORE INTO user_roles (telegram_id) VALUES (?)", (tg_id,)
    )
    await db.commit()