import logging

from aiosqlite import Connection

logger = logging.getLogger(__name__)


async def get_role(db: Connection, tg_id: int) -> str:
    async with db.execute(
        "SELECT role FROM user_roles WHERE telegram_id = ?", (tg_id,)
    ) as cursor:
        return await cursor.fetchone()


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


async def ban_user(db: Connection, self_id: int, tg_id: int, cause: str | None) -> str:
    role = get_role(db=db, tg_id=self_id)
    if role not in ("creator", "moder"):
        return f"Ты не можешь банить, твоя роль: {role}"

    if cause is not None:
        query = "INSERT INTO bans (telegram_id, cause) VALUES (?, ?)"
        params = (tg_id, cause)
    else:
        query = "INSERT INTO bans (telegram_id, cause) VALUES (?)"
        params = (tg_id,)

    async with db.execute(query, params) as cursor:
        row = await cursor.fetchone()
        await db.commit()
        if row is not None:
            return f"Пользователь забанен\nЮзернейм: {row['username']}\n\
            Дата регистрации: {row['registration_date']}\nПричина: {cause if cause is not None else "Админ так решил."}"
        else:
            return
