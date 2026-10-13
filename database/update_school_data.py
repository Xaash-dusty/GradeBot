from aiosqlite import Connection


async def update_persons(
    db: Connection, persons: list[tuple[int, int, str, str]]
) -> None:
    query = "INSERT OR IGNORE INTO persons (person_id, user_id, name, sex) VALUES (?, ?, ?, ?)"
    await db.executemany(query, persons)
    await db.commit()


async def update_subjects(db: Connection, subjects: list[tuple[int, str]]) -> None:
    query = "INSERT OR IGNORE INTO subjects (subject_id, name) VALUES (?, ?)"
    await db.executemany(query, subjects)
    await db.commit()


async def update_lessons(
    db: Connection, lessons: list[tuple[int, int, str, str]]
) -> None:
    query = "INSERT OR IGNORE INTO lessons (lesson_id, subject_id, title, date) VALUES (?, ?, ?, ?)"
    await db.executemany(query, lessons)
    await db.commit()


async def update_work_types(
    db: Connection, work_types: list[tuple[int, str, str, int]]
) -> None:
    query = "INSERT OR IGNORE INTO work_types (work_type_id, kind, title, weight) VALUES (?, ?, ?, ?)"
    await db.executemany(query, work_types)
    await db.commit()


async def update_works(db: Connection, works: list[tuple[int, int, int]]) -> None:
    query = "INSERT OR IGNORE INTO works (work_id, lesson_id, type_id) VALUES (?, ?, ?)"
    await db.executemany(query, works)
    await db.commit()


async def update_marks(db: Connection, marks: list[tuple[int, int, int, int]]) -> None:
    query = """INSERT INTO marks (mark_id, person_id, work_id, value) VALUES (?, ?, ?, ?)
        ON CONFLICT (mark_id) DO UPDATE SET value = excluded.value"""
    await db.executemany(query, marks)
    await db.commit()
