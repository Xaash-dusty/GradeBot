import asyncio
import logging
import os
from pathlib import Path

import aiosqlite
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from database.initialization import init_db
from handlers.common import router as common_router
from handlers.dnevnik_connection import router as link_dnevnik_router
from handlers.fallbacks import router as fallbacks_router
from middlewares.db_middleware import DatabaseMiddleware
from updater import auto_update_db

# 1. ---------------- Логеры ------------------

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("aiosqlite").setLevel(logging.ERROR)
logging.getLogger("aiogram.event").setLevel(logging.WARNING)

formatter = logging.Formatter(
    fmt="%(asctime)s - [%(name)s] - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d-%H:%M:%S",
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

session_file_handler = logging.FileHandler(
    filename="logs/sessional_logs.log", mode="w", encoding="utf-8"
)
session_file_handler.setLevel(logging.DEBUG)
session_file_handler.setFormatter(formatter)


timeless_file_handler = logging.FileHandler(
    filename="logs/timeless_logs.log", mode="a", encoding="utf-8"
)
timeless_file_handler.setLevel(logging.DEBUG)
timeless_file_handler.setFormatter(formatter)


root_logger.addHandler(console_handler)
root_logger.addHandler(session_file_handler)
root_logger.addHandler(timeless_file_handler)

logger = logging.getLogger(__name__)

# 2. ------------------ ТОКЕН и запуск бота -------------------

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if TOKEN is None:
    logger.critical("The Token is not set")
    raise RuntimeError("The Token is not found")

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def periodic_update(db: aiosqlite.Connection, interval: int) -> None:
    while True:
        await auto_update_db(db=db)
        await asyncio.sleep(interval)


async def main():
    dp.include_routers(common_router, link_dnevnik_router, fallbacks_router)

    DB_DIR = Path(__file__).resolve().parent / "data" / "database.db"
    async with aiosqlite.connect(DB_DIR) as db:
        db.row_factory = aiosqlite.Row
        await init_db(db=db)
        asyncio.create_task(periodic_update(db=db, interval=120))

        dp.message.middleware(DatabaseMiddleware(db))
        dp.callback_query.middleware(DatabaseMiddleware(db))

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
