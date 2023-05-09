from typing import Any, List


import aiohttp

from app.schemas.message import MessageInDB

from datetime import datetime

from app.sheduler.requests import (
    send_message
)

from app.sheduler.datatypes import (
    Message,
    MessagePool
)

from app.sheduler.exceptions import BadResponse


DEFAULT_TIMEZONE = datetime.now().tzinfo()


async def send_awaited_messages(
    aiohttp_session: aiohttp.ClientSession,
    url: str,
    token: str,
    message_pool: MessagePool,
):
    while message_pool.messages:
        message: Message = message_pool.messages.pop(0)
        now = datetime.now(DEFAULT_TIMEZONE)
        try:
            if now > message.start_window:
                if message.end_window:
                    if now < message.end_window:
                        # message has both start and end marks and fit in them
                        await send_message(
                            message.message_object.dict(),
                            url,
                            token
                        )
                    else:
                        # its too late to send message
                        pass
                else:
                    # message has only start mark and fit in 
                    await send_message(
                        message.message_object.dict(),
                        url,
                        token
                    )
            else:
                # it's to early to send message
                message_pool.messages.append(message)
        except BadResponse as e:
            # something wrong with reciever
            print(e)
            pass
