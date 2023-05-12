from typing import List
from asyncpg import Connection
import ujson

from app.schemas.mailing import (
    MailingCreate,
    MailingInDB,
    MailingUpdate,
)

from app.db.base import DatabaseManager as DM


@DM.acquire_connection()
async def get_active(
    conn: Connection = None,
) -> List[MailingInDB]:
    result = await conn.fetch(
        'select * from available_mailings'
    )
    if not result:
        return
    mailings = [MailingInDB(**mailing) for mailing in result]
    return mailings


@DM.acquire_connection()
async def statistic_short(
    conn: Connection = None,
) -> List[dict]:
    await conn.set_type_codec(
        'json',
        encoder=ujson.dumps,
        decoder=ujson.loads,
        schema='pg_catalog',
    )
    result = await conn.fetch(
        '''
            select
                mailing.*,
                message_status_stats.status,
                (now() between mailing.start_time and mailing.end_time)
                as is_active_now
            from
                message_status_stats
            left join
                mailing
            on
                message_status_stats.mailing_id = mailing.id
        ''')
    if not result:
        return
    stats = [dict(stat) for stat in result]
    return stats


@DM.acquire_connection()
async def statistic_verbose(
    mailing_id: int,
    conn: Connection = None,
) -> dict:
    await conn.set_type_codec(
        'json',
        encoder=ujson.dumps,
        decoder=ujson.loads,
        schema='pg_catalog',
    )
    result = await conn.fetch(
        '''
            select
                array_agg(message.*) messages,
                min(message.time_created) as first_sended,
                max(message.time_created) as last_sended
            from
                message
            where
                mailing_id = $1
            group by
                status
        ''',
        mailing_id,
    )
    if not result:
        return
    stats = [dict(stat) for stat in result]
    return stats


@DM.acquire_connection()
async def update(
    id: int,
    mailing_data: MailingUpdate,
    conn: Connection = None,
) -> MailingInDB:
    await conn.set_type_codec(
        'json',
        encoder=ujson.dumps,
        decoder=ujson.loads,
        schema='pg_catalog',
    )
    result = await conn.fetchrow(
        'update mailing '
            'set start_time = $1, '
            'end_time = $2, '
            'body = $3, '
            'filters = $4::json, '
        'where id = $7 returning *',
        mailing_data.start_time,
        mailing_data.end_time,
        mailing_data.body,
        mailing_data.filters,
        id,
    )
    if not result:
        return
    mailing = MailingInDB(**result)
    return mailing


@DM.acquire_connection()
async def delete(
    id: int,
    conn: Connection = None,
) -> MailingInDB:
    await conn.set_type_codec(
        'json',
        encoder=ujson.dumps,
        decoder=ujson.loads,
        schema='pg_catalog',
    )
    result = await conn.fetchrow(
        'delete from mailing '
        'where id = $1 returning *',
        id,
    )
    if not result:
        return
    mailing = MailingInDB(**result)
    return mailing


@DM.acquire_connection()
async def create(
    mailing_data: MailingCreate,
    conn: Connection = None,
) -> MailingInDB:
    await conn.set_type_codec(
        'json',
        encoder=ujson.dumps,
        decoder=ujson.loads,
        schema='pg_catalog',
    )
    result = await conn.fetchrow(
        'insert into mailing '
        '(start_time, end_time, body, filters ) values '
        '( $1, $2, $3, $4::json) returning * ',
        mailing_data.start_time,
        mailing_data.end_time,
        mailing_data.body,
        mailing_data.filters
    )
    if not result:
        return
    mailing = MailingInDB(**result)
    return mailing
