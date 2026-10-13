import logging

from aiosqlite import Connection

logger = logging.getLogger(__name__)


async def change_role(db: Connection, tg_id: int, new_role: str) -> None:
    async with db.execute(
        """SELECT u.telegram_id AS tg_id, u.first_name AS first_name, u.username AS username, r.name AS old_role, r_n.id AS new_role_id
        FROM users AS u
        LEFT JOIN user_roles AS u_r ON u.telegram_id = u_r.telegram_id
        LEFT JOIN roles AS r ON r.id = u_r.role_id
        LEFT JOIN roles AS r_n ON r_n.name = ?
        WHERE tg_id = ?
        """,
        (new_role, tg_id),
    ) as cursor:
        row = await cursor.fetchone()
        if row is None:
            logger.warning(
                f"При попытке изменить роль не удалось найти пользователя с {tg_id = }"
            )
            return
        if not row["new_role_id"]:
            logger.warning(
                f"При попытке изменить роль не удалось найти роль {new_role = }"
            )
            return

        await db.execute(
            "UPDATE user_roles SET role_id = ? WHERE telegram_id = ?",
            (row["new_role_id"], tg_id),
        )
        await db.commit()
        logger.info(
            f"Роль пользователя изменена\n{row['first_name'] = }\t{row['username'] = }\t{row['old_role'] = }\t{new_role = }"
        )


async def ban_user(db: Connection, tg_id: int, cause: str | None) -> None:
    if cause is not None:
        query = "INSERT OR IGNORE INTO bans (telegram_id, cause) VALUES (?, ?) RETURNING telegram_id AS tg_id, cause"
        params = (tg_id, cause)
    else:
        query = "INSERT OR IGNORE INTO bans (telegram_id) VALUES (?) RETURNING telegram_id AS tg_id, cause"
        params = (tg_id,)

    async with db.execute(query, params) as cursor:
        row = await cursor.fetchone()
        if row is not None:
            logger.info(f"Пользователь забанен\n{row['tg_id'] = }\t{row['cause'] = }")
        await db.commit()