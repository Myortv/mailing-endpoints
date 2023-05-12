from typing import List, Dict
from asyncpg import Connection
from fastapi import HTTPException

from app.schemas.client import (
    ClientInDB,
    ClientFliter,
    ClientCreate,
)
from app.db.base import DatabaseManager as DM, generate_placeholder


@DM.acquire_connection()
async def get_all_clients(
    conn: Connection = None,
) -> List[ClientInDB]:
    result = await conn.fetch(
        'select * from client '
    )
    if not result:
        return
    clients = [ClientInDB(**client) for client in result]
    return clients


@DM.acquire_connection()
async def update(
    id: int,
    client: ClientCreate,
    conn: Connection = None,
) -> ClientInDB:
    result = await conn.fetchrow(
        'update client '
            'set phone_number = $1, '
            'mobile_operator_code = $2, '
            'tag = $3, '
            'timezone = $4, '
            'start_recieve = $5, '
            'recieve_duration = $6 '
        'where id = $7 returning *',
        client.phone_number,
        client.mobile_operator_code,
        client.tag,
        client.timezone,
        client.start_recieve,
        client.recieve_duration,
        id,
    )
    if not result:
        return
    client = ClientInDB(**result)
    return client


@DM.acquire_connection()
async def get_filtered(
    filter: ClientFliter,
    conn: Connection = None,
) -> List[ClientInDB]:
    placeholder, values = generate_placeholder(filter)
    result = await conn.fetch(
        'select * from client where '
        f"{' and '.join(placeholder)}",
        *values
    )
    if not result:
        return
    clients = [ClientInDB(**client) for client in result]
    return clients


@DM.acquire_connection()
async def delete(
    id: int,
    conn: Connection = None,
) -> ClientInDB:
    result = await conn.fetchrow(
        'delete from client '
        'where id = $1 returning *',
        id,
    )
    if not result:
        return
    client = ClientInDB(**result)
    return client


@DM.acquire_connection()
async def create(
    client: ClientCreate,
    conn: Connection = None,
) -> ClientInDB:
    result = await conn.fetchrow(
        'insert into client '
        '(phone_number, mobile_operator_code, tag, timezone, '
        'start_recieve, recieve_duration) values '
        '( $1, $2, $3, $4, $5, $6 ) returning * ',
        client.phone_number,
        client.mobile_operator_code,
        client.tag,
        client.timezone,
        client.start_recieve,
        client.recieve_duration,
    )
    if not result:
        return
    client = ClientInDB(**result)
    return client

@DM.acquire_connection()
async def get_active(
    conn: Connection = None,
) -> List[ClientInDB]:
    result = await conn.fetch(
        'select * from available_clients'
    )
    if not result:
        return
    clients = [ClientInDB(**client) for client in result]
    return clients


# @DM.acquire_connection()
# async def get_free_clients(
#     mailing_id: int,
#     filters: ClientFliter,
#     conn: Connection = None,
# ) -> List[ClientInDB]:
#     placeholder, values = generate_placeholder(filters, i=1)
#     condition = ''
#     for line in placeholder:
#         condition += f'and {line}'
#     # logging.debug(f'\t\tinside get free clients. placeholder: {placeholder}')
#     result = await conn.fetch(
#         'select '
#             'id, '
#             'mobile_operator_code, '
#             'tag, '
#             'timezone, '
#             'start_recieve at time zone timezone as start_recieve, '
#             'recieve_duration, '
#             'phone_number '
#         'from '
#         'available_clients '
#             'where '
#             '(available_clients.id in (select client_id from message) and '
#             f'$1 in (select mailing_id from message)) = false {condition} ',
#         mailing_id,
#         *values
#     )
#     if not result:
#         return
#     clients = [ClientInDB(**client) for client in result]
#     return clients
