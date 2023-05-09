from fastapi import HTTPException

from app.schemas.client import ClientInDB

from app.db.base import DatabaseManager as DM


@DM.acquire_connection()
async def get_all_clients(conn=None):
    result = await conn.fetch(
        'select * from client '
    )
    if not result:
        raise HTTPException(404)
    clients = [ClientInDB(**client) for client in result]
    return clients
