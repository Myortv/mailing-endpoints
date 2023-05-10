from typing import List

import aiohttp

from datetime import datetime

from app.sheduler.requests import (
    send_message
)

from app.sheduler.datatypes import (
    Message,
    MessageRequest,
    MessageResponse,
    Mailing,
)

from
from app.sheduler.exceptions import BadResponse


import logging


async def mailing_task(
    mailing_task: Mailing,
    token: str = None,  # create token as dep
    url: str = None,  # create url as dep
):
    logging.info('\t\t----------------------- SERVING MAILING TASK ---------------------')
    # create session here
    # aiohttp_session: aiohttp.ClientSession,
    logging.info('\t\t----------------------- START AIOHTTP SESSION ---------------------')
    message_queue = mailing_task.message_queue
    now = datetime.now(message_queue[0].start_window.tzinfo)
    async with aiohttp.ClientSession() as session:
        while message_queue:
            message: Message = message_queue.pop(0)
            try:
                if now > message.start_window:
                    if message.end_window:
                        if now < message.end_window:
                            # message has both start and end marks and fit in them
                            
                            await send_message(
                                MessageRequest(),
                                url,
                                token
                            )
                        else:
                            # its too late to send message
                            continue
                    else:
                        await send_message(
                            message.message_object.dict(),
                            url,
                            token
                        )
                else:
                    # it's to early to send message
                    message_queue.append(message)
            except BadResponse as e:
                # something wrong with reciever
                logging.warning(e)
                pass
            except Exception as e:
                # something wrong with the code
                logging.warning(e.__str__())
