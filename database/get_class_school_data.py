from aiosqlite import Connection


async def get_subjects(db: Connection):
    async with db.execute(
        "SELECT s.name AS subject FROM subjects AS s WHERE s.subject_id != 2545537322856967580 AND s.subject_id != 2546480403185888746"
    ) as cursor:
        rows = await cursor.fetchall()
        return rows
