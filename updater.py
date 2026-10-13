import asyncio
import logging
import os
import time
from datetime import date, timedelta
from pathlib import Path

import aiohttp
from aiosqlite import Connection, connect
from dotenv import load_dotenv

from database.initialization import init_db
from database.update_school_data import (
    update_lessons,
    update_marks,
    update_persons,
    update_subjects,
    update_work_types,
    update_works,
)

logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("DNEVNIK_API_TOKEN")
if TOKEN is None:
    logger.error("DNEVNIK_API_TOKEN is not set")
    raise RuntimeError("DNEVNIK_API_TOKEN is not found")


HEADERS = {"Access-Token": TOKEN}
GROUP = os.getenv("GROUP_ID")
SCHOOL = os.getenv("SCHOOL_ID")


async def auto_update_db(db: Connection) -> None:
    """Automatic update of all tables"""
    try:
        start = time.perf_counter()

        async with aiohttp.ClientSession(
            base_url="https://api.dnevnik.ru/v2.0/",
            headers=HEADERS,
            raise_for_status=True,
        ) as session:
            # Получаем работы из уроков, т.к. специального эндпоинта для получения всех работ нет
            new_data = await asyncio.gather(
                get_marks(session=session),
                get_persons(session=session),
                get_subjects(session=session),
                get_work_types(session=session),
                get_lessons_and_works(session=session),
            )

            marks, persons, subjects, work_types, lessons_and_works = new_data
            await update_marks(db=db, marks=marks)
            await update_persons(db=db, persons=persons)
            await update_subjects(db=db, subjects=subjects)
            await update_work_types(db=db, work_types=work_types)
            await update_lessons(db=db, lessons=lessons_and_works[0])
            await update_works(db=db, works=lessons_and_works[1])

    except aiohttp.ClientResponseError as e:
        logger.exception(
            f"API вернул HTTP-ошибку {e.status} по url {e.request_info.url}"
        )

    except (TimeoutError, aiohttp.ClientError, aiohttp.ClientConnectionError):
        logger.exception("Ошибка соединения с API")

    except (TypeError, ValueError, KeyError):
        logger.exception("Некорректные данные от API")

    except Exception:
        logger.exception("Неожиданная ошибка при обновлении БД")

    else:
        logger.info(
            f"Database was updated. The update took {time.perf_counter() - start:.2f}s"
        )


async def get_persons(
    session: aiohttp.ClientSession,
) -> list[tuple[int, int, str, str]]:
    url = f"edu-groups/{GROUP}/persons"
    async with session.get(url) as response:
        persons = await response.json()
        return [(p["id"], p["userId"], p["shortName"], p["sex"]) for p in persons]


async def get_subjects(session: aiohttp.ClientSession) -> list[tuple[int, str]]:
    url = f"edu-groups/{GROUP}/subjects"
    async with session.get(url) as response:
        subjects = await response.json()
        return [(s["id"], s["name"]) for s in subjects]


async def get_lessons_and_works(
    session: aiohttp.ClientSession,
) -> tuple[list[tuple[int, int, str, str]], list[tuple[int, int, int]]]:
    date_from = "2026-09-01"
    today = date.today()
    date_to = str(today + timedelta(days=14))
    url = f"edu-groups/{GROUP}/lessons/{date_from}/{date_to}"

    async with session.get(url) as response:
        row_lessons = await response.json()
        works = [
            (w["id"], w["lesson"], w["workType"])
            for l in row_lessons
            for w in l["works"]
        ]
        lessons = [
            (l["id"], l["subject"]["id"], l["title"], l["date"]) for l in row_lessons
        ]

    return (lessons, works)


async def get_work_types(
    session: aiohttp.ClientSession,
) -> list[tuple[int, str, str, int]]:
    url = f"work-types/{SCHOOL}"
    async with session.get(url) as response:
        work_types = await response.json()
        return [
            (w_t["id"], w_t["kind"], w_t["title"], int(w_t["weight"]))
            for w_t in work_types
            if "weight" in w_t
        ]


async def get_marks(session: aiohttp.ClientSession) -> list[tuple[int, int, int, int]]:
    date_from = "2026-09-01"
    today = date.today()
    date_to = str(today + timedelta(days=14))
    url = f"edu-groups/{GROUP}/marks/{date_from}/{date_to}"
    async with session.get(url) as response:
        marks = await response.json()
        return [(m["id"], m["person"], m["work"], int(m["value"][0])) for m in marks]


async def main():
    DB_DIR = Path(__file__).resolve().parent / "data" / "beta_database.db"
    async with connect(DB_DIR) as db:
        await init_db(db=db)
        await auto_update_db(db=db)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("aiosqlite").setLevel(logging.ERROR)

    asyncio.run(main())
