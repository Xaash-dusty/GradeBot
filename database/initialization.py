import asyncio
import logging
from pathlib import Path

import aiosqlite

logger = logging.getLogger(__name__)


async def init_db(db: aiosqlite.Connection) -> None:
    create_tables_query = """
    CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL UNIQUE,
    user_id INTEGER NOT NULL UNIQUE,
    name TEXT NOT NULL UNIQUE,
    sex TEXT NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY,
    subject_id INTEGER NOT NULL UNIQUE,
    name TEXT NOT NULL UNIQUE
    );
    
    CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY,
    lesson_id INTEGER NOT NULL UNIQUE,
    subject_id INTEGER NOT NULL,
    title TEXT,
    date TEXT,
    FOREIGN KEY (subject_id) REFERENCES subjects (subject_id)
    );

    CREATE TABLE IF NOT EXISTS work_types (
    id INTEGER PRIMARY KEY,
    work_type_id INTEGER NOT NULL UNIQUE,
    kind TEXT NOT NULL,
    title TEXT NOT NULL,
    weight INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS works (
    id INTEGER PRIMARY KEY,
    work_id INTEGER NOT NULL UNIQUE,
    lesson_id INTEGER NOT NULL,
    type_id INTEGER NOT NULL,
    FOREIGN KEY (lesson_id) REFERENCES lessons (lesson_id),
    FOREIGN KEY (type_id) REFERENCES work_types (work_type_id)
    );

    CREATE TABLE IF NOT EXISTS marks (
    id INTEGER PRIMARY KEY,
    mark_id INTEGER NOT NULL UNIQUE,
    person_id INTEGER NOT NULL,
    work_id INTEGER NOT NULL,
    value INTEGER NOT NULL,
    FOREIGN KEY (person_id) REFERENCES persons (person_id),
    FOREIGN KEY (work_id) REFERENCES works (work_id)
    );


    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    telegram_id INTEGER NOT NULL UNIQUE,
    username TEXT UNIQUE,
    first_name TEXT NOT NULL,
    registration_date TEXT NOT NULL DEFAULT (datetime('now')),
    last_activity TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS user_roles (
    id INTEGER PRIMARY KEY,
    telegram_id INTEGER NOT NULL UNIQUE,
    role TEXT NOT NULL DEFAULT 'guest',
    FOREIGN KEY (telegram_id) REFERENCES users (telegram_id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS bans (
    id INTEGER PRIMARY KEY,
    telegram_id INTEGER NOT NULL UNIQUE,
    cause TEXT NOT NULL DEFAULT 'Админ так решил.',
    ban_date TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (telegram_id) REFERENCES users (telegram_id) ON DELETE CASCADE
    );
    """

    await db.executescript(create_tables_query)
    await db.commit()
    logger.info("Database has been initialized")


async def main():
    DB_DIR = Path(__file__).resolve().parent.parent / "debugging" / "beta_database.db"
    async with aiosqlite.connect(DB_DIR) as db:
        await init_db(db=db)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("aiosqlite").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    asyncio.run(main())
