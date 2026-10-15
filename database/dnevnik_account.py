import logging

from aiosqlite import Connection

logger = logging.getLogger(__name__)


async def get_account_status(db: Connection, tg_id: int) -> str:
    async with db.execute(
            "SELECT is_active FROM user_accounts WHERE telegram_id = ? LIMIT 1", (tg_id,)
        ) as cursor:
        row = await cursor.fetchone()
        if row is None: return "None"
        return "active" if row["is_active"] == 1 else "inactive"


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
