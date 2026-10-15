from aiosqlite import Connection


async def get_subjects(db: Connection):
    async with db.execute(
        "SELECT subjects.name AS subject FROM subjects WHERE subjects.subject_id != 2545537322856967580"
    ) as cursor:
        rows = await cursor.fetchall()
        return rows