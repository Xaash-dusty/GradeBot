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
            logger.info(
                f"Новый пользователь\n{tg_id = }\t{first_name = }\t{username = }"
            )

    async with db.execute(
        "INSERT OR IGNORE INTO user_roles (telegram_id) VALUES (?) RETURNING role_id",
        (tg_id,),
    ) as cursor:
        row = await cursor.fetchone()
        if row is not None:
            logger.info(
                f"Пользователю установлена новая роль\n{tg_id = }\t{first_name = }\t{username = }\t{row['role_id'] = }"
            )
    await db.commit()


async def get_person_id_by_password(db: Connection, password: str) -> int | None:
    async with db.execute(
        "SELECT person_id FROM person_passwords WHERE password = ?", (password,)
    ) as cursor:
        row = await cursor.fetchone()
        logger.debug(
            f"Попытка получить person_id по паролю\n{password = }\t{row['person_id'] = }"
        )
        return row["person_id"] if row is not None else None


async def is_valid_person_id(db: Connection, person_id: int) -> bool:
    query = """SELECT u_a.telegram_id AS linked_id FROM persons AS p
            LEFT JOIN user_accounts AS u_a ON u_a.person_id = p.person_id
            WHERE p.person_id = ?"""
    async with db.execute(query, (person_id,)) as cursor:
        row = await cursor.fetchone()
        return row is not None and row["linked_id"] is None


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
