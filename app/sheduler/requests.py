from typing import Any

import aiohttp

import ujson

from app.sheduler.exceptions import (
        BadResponse
    )


async def send_message(
    data: dict,
    url: str,
    auth_token: str,
):
    headers = dict()
    headers['Authorization'] = f'Bearer {auth_token}'
    body = ujson.dumps(data)
    with aiohttp.ClientSession() as session:
        response = await session.post(
            url,
            headers=headers,
            json=body,
        )
        if response.status != 200:
            raise BadResponse(response)
    return response