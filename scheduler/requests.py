from typing import Any

import aiohttp

import ujson

from scheduler.exceptions.exceptions import (
        BadResponse
    )

import logging


async def send_message(
    data: dict,
    url: str,
    auth_token: str,
):
    logging.info('\t\t----------------------- SENDING MESSAGE ---------------------')
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
