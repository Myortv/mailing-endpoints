from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer

from fastapi_auth0 import Auth0, Auth0User

from app.core.configs import settings

from app.controllers import client
from app.schemas.client import (
    ClientInDB,
    ClientCreate,
    ClientUpdate,
    ClientInDB,
    ClientFliter,
)

auth = settings.AUTH
router = APIRouter()


@router.get('/client/admin/all', response_model=List[client.ClientInDB])
async def get_all_clients(
    user: Auth0User = Depends(auth.get_user),
) -> List[client.ClientInDB]:
    result = await client.get_all_clients()
    if not result:
        raise HTTPException(404)
    return result


@router.post('/client/get-filtered/', response_model=List[client.ClientInDB])
async def get_filtered(
    filter: ClientFliter,
):
    result = await client.get_filtered(filter)
    if not result:
        raise HTTPException(404)
    return result


@router.get('/client/active', response_model=List[client.ClientInDB])
async def get_active_clients():
    """
        return clients that recieve messages right now
    """
    result = await client.get_active()
    if not result:
        raise HTTPException(404)
    return result


@router.post('/client/', response_model=ClientInDB)
async def create(
    client_data: ClientCreate
):
    result = await client.create(client_data)
    if not result:
        raise HTTPException(404)
    return result


@router.put('/client/', response_model=client.ClientInDB)
async def update(
    id: int,
    client_data: ClientUpdate,
):
    result = await client.update(id, client_data)
    if not result:
        raise HTTPException(404)
    return result


@router.delete('/client/', response_model=client.ClientInDB)
async def delete(
    id: int,
):
    result = await client.delete(id)
    if not result:
        raise HTTPException(404)
    return result
