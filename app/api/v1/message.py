from typing import List
from fastapi import APIRouter, HTTPException

from app.controllers import message
from app.schemas.message import (
    MessageCreate,
    MessageUpdate,
    MessageInDB,
)


router = APIRouter()

