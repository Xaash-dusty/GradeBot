import logging

from aiosqlite import Connection

logger = logging.getLogger(__name__)


async def is_valid_person_id(db: Connection, person_id: int) -> bool:
    query = """SELECT u_a.telegram_id AS linked_id FROM persons AS p
            LEFT JOIN user_accounts AS u_a ON u_a.person_id = p.person_id
            WHERE p.person_id = ?"""
    async with db.execute(query, (person_id,)) as cursor:
        row = await cursor.fetchone()
        return row is not None and row["linked_id"] is None


async def has_any_account(db: Connection, tg_id: int) -> bool:
    async with db.execute(
        "SELECT 1 FROM user_accounts WHERE telegram_id = ? LIMIT 1", (tg_id,)
    ) as cursor:
        row = await cursor.fetchone()
        return row is not None


async def is_active_account(db: Connection, tg_id: int) -> bool:
    async with db.execute(
        "SELECT is_active FROM user_accounts WHERE telegram_id = ? LIMIT 1", (tg_id,)
    ) as cursor:
        row = await cursor.fetchone()
        return row["is_active"] == 1


async def link_dnevnik(db: Connection, tg_id: int, person_id: int) -> bool:
    async with db.execute(
        "INSERT OR IGNORE INTO user_accounts (telegram_id, person_id) VALUES (?, ?)"
        "RETURNING id, creation_date",
        (tg_id, person_id),
    ) as cursor:
        row = await cursor.fetchone()
        await db.commit()
        if row is None:
            logger.error(
                f"Пользователь не смог привязать дневник\n{tg_id = }\t{person_id = }"
            )
            return False

        logger.info(
            f"Пользователь привязал дневник\n{tg_id = }\t{person_id = }\n{row['id'] = }\t{row['creation_date'] = }"
        )
        return True


async def activate_dnenik(db: Connection, tg_id: int) -> None:
    async with db.execute(
        "UPDATE user_accounts SET is_active = 1 WHERE telegram_id = ?"
        "RETURNING person_id",
        (tg_id,),
    ) as cursor:
        row = await cursor.fetchone()
        await db.commit()
        logger.info(
            f"Пользователь активировал дневник\n{tg_id = }\t{row['person_id'] = }"
        )


async def deactivate_dnevnik(db: Connection, tg_id: int) -> None:
    async with db.execute(
        "UPDATE user_accounts SET is_active = 0 WHERE telegram_id = ?"
        "RETURNING person_id",
        (tg_id,),
    ) as cursor:
        row = await cursor.fetchone()
        await db.commit()
        logger.info(
            f"Пользователь деактивировал дневник\n{tg_id = }\t{row['person_id'] = }"
        )
