from typing import List
from fastapi import APIRouter, HTTPException

from app.controllers import mailing
from app.schemas.mailing import (
    MailingInDB,
    MailingCreate,
    MailingUpdate,
)


router = APIRouter()


@router.get('/mailing/stats/short')
async def statistic_short() -> List[dict]:
    """
        return statistic of all created mailings
        with short statistic messages status
    """
    result = await mailing.statistic_short()
    if not result:
        raise HTTPException(404)
    return result


@router.get('/mailing/stats/verbose')
async def statistic_verbose(id: int) -> List[dict]:
    """
        return statistic of single mailing
        including all messages grouped by status
    """
    result = await mailing.statistic_verbose(id)
    if not result:
        raise HTTPException(404)
    return result


@router.get('/mailing/active')
async def get_running_mailings() -> List[MailingInDB]:
    """
        return still running mailings
    """
    result = await mailing.active()
    if not result:
        raise HTTPException(404)
    return result


@router.post('/mailing/')
async def create_mailing(
    mailing_data: MailingCreate,
) -> MailingInDB:
    """
        create new mailing
    """
    result = await mailing.create(mailing_data)
    if not result:
        raise HTTPException(404)
    return result


@router.put('/mailing/')
async def update_mailing(
    id: int,
    mailing_data: MailingUpdate,
) -> MailingInDB:
    """
        update exsisting mailing
    """
    result = await mailing.update(id, mailing_data)
    if not result:
        raise HTTPException(404)
    return result


@router.delete('/mailing/')
async def delete_mailing(
    id: int,
) -> MailingInDB:
    """
        delete exsisting mailing
    """
    result = await mailing.delete(id)
    if not result:
        raise HTTPException(404)
    return result
