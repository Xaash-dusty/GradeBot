from aiosqlite import Connection, Row


async def get_person_marks(db: Connection, person_id: int) -> list[Row]:
    query = ""