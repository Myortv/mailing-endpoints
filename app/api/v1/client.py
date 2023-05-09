from typing import List

from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPBearer

from fastapi_auth0 import Auth0, Auth0User

from app.core.configs import settings

from app.controllers import client
from app.schemas.client import (
    ClientInDB,
    ClientCreate,
    ClientUpdate,
)

auth = settings.AUTH
router = APIRouter()


@router.get('/client/admin/all', response_model=List[client.ClientInDB])
async def get_all_clients(
    user: Auth0User = Depends(auth.get_user),
) -> List[client.ClientInDB]:
    return await client.get_all_clients()
