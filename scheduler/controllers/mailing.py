from fastapi import HTTPException

from scheduler.schemas.mailing import MailingInDB

from scheduler.db.base import DatabaseManager as DM

from asyncpg import Connection


@DM.acquire_connection()
async def get_nearest_mailing(
    conn: Connection = None,
):
    result = await conn.fetch(
        '''select
            *
        from
            mailing
        where
            (
                mailing.end_time is not null and
                now() between
                    mailing.start_time
                        and
                    mailing.end_time
            ) or (
                now() > mailing.start_time and
                mailing.end_time is null
            )'''
        )
    if not result:
        return
    mailings = [MailingInDB(**mailing) for mailing in result]
    return mailings
