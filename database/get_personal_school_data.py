from aiosqlite import Connection, Row


async def get_user_marks(db: Connection, tg_id: int) -> list[Row]:
    query = """
        SELECT s.name AS subject, GROUP_CONCAT(m.value, ' ' ORDER BY l.date, m.mark_id) AS marks,
            PRINTF('%.2f', SUM(m.value * wt.weight) * 1.0 / SUM(wt.weight)) AS wa_score
        FROM marks AS m
        INNER JOIN persons AS p ON p.person_id = m.person_id
        INNER JOIN user_accounts AS ua ON ua.person_id = p.person_id
        INNER JOIN works AS w ON w.work_id = m.work_id
        INNER JOIN work_types AS wt ON wt.work_type_id = w.type_id
        INNER JOIN lessons AS l ON l.lesson_id = w.lesson_id
        INNER JOIN subjects AS s ON s.subject_id = l.subject_id
        WHERE ua.telegram_id = ?
        GROUP BY s.subject_id
        ORDER BY s.name
        """
    async with db.execute(query, (tg_id,)) as cursor:
        rows = await cursor.fetchall()
        return rows


async def get_subject_id(db: Connection, subject: str) -> int | None:
    async with db.execute("SELECT subject_id FROM subjects WHERE name = ? LIMIT 1", (subject,)) as cursor:
        row = await cursor.fetchone()
        return row['subject_id'] if row is not None else None


async def get_user_subject_marks(db: Connection, tg_id: int, subject_id: int) -> list[Row]:
    query = """
        SELECT s.name AS subject, m.value AS mark, wt.weight AS weight,
        wt.title AS type, l.title AS title, l.date AS date FROM marks AS m
        INNER JOIN persons AS p ON p.person_id = m.person_id
        INNER JOIN user_accounts AS ua ON ua.person_id = p.person_id
        INNER JOIN works AS w ON w.work_id = m.work_id
        INNER JOIN work_types AS wt ON wt.work_type_id = w.type_id
        INNER JOIN lessons AS l ON l.lesson_id = w.lesson_id
        INNER JOIN subjects AS s ON s.subject_id = l.subject_id
        WHERE ua.telegram_id = ? AND s.subject_id = ?
        ORDER BY date
        """
    async with db.execute(query, (tg_id, subject_id)) as cursor:
        rows = await cursor.fetchall()
        return rows