from typing import Any

import aiohttp

import ujson

from scheduler.exceptions.exceptions import (
        BadResponse
    )

from scheduler.schemas.message import MessageResponse

from scheduler.core.configs import settings

import logging


async def send_message(
    data: dict,
    url: str = settings.MAILING_SERVER_URL,
    auth_token: str = settings.AUTHTOKEN,
):
    logging.info('\t\t----------------------- SENDING MESSAGE ---------------------')
    headers = dict()
    headers['Authorization'] = f'Bearer {auth_token}'
    headers['accept'] = 'application/json'
    headers['Content-Type'] = 'application/json'
    body = ujson.dumps(data)
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{url}{data['id']}",
            headers=headers,
            # json=body,
            json=data,
        ) as response:
            if response.status != 200:
                raise BadResponse(response)
            return MessageResponse.parse_raw(await response.text())
