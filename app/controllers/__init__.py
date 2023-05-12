from asyncpg import Connection
from app.db.base import DatabaseManager as DM

@DM.acquire_connection()
async def fetch_timezones(conn: Connection = None):
    result = await conn.fetch(
        'SELECT '
            'name, '
            'abbrev, '
            'utc_offset, '
            'is_dst '
        'FROM pg_timezone_names '
        "WHERE name !~ 'posix' "
        'ORDER BY name asc'
    )
    abbrev = [row['abbrev'] for row in result]
    offset = [row['utc_offset'] for row in result]
    names = [row['name'] for row in result]

    return frozenset(abbrev + offset + names)
