from fastapi import HTTPException

from typing import List

import aiohttp

from datetime import datetime

import asyncio

from scheduler.requests import (
    send_message
)

from scheduler.controllers.message import create_message, change_status

from scheduler.schemas.datatypes import (
    Mailing,
    Message,
)


from scheduler.schemas.message import (
    MessageRequest,
    MessageResponse,
    MessageCreate,
)
from scheduler.exceptions.exceptions import BadResponse

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
                            logging.info('\t\t----------------------- CREATE MESSAGE IN DB ---------------------')
                            message_in_db = await create_message(
                                MessageCreate(
                                    mailing_id=mailing_task.id,
                                    client_id=message.client_id,
                                )
                            )
                            logging.info('\t\t----------------------- MESSAGE CREATED IN DB ---------------------')
                            logging.info('\t\t----------------------- SEND MESSAGE TO SERVICE ---------------------')
                            await send_message(
                                MessageRequest(
                                    id=message_in_db.id,
                                    phone=message.phone,
                                    text=mailing_task.body
                                ).dict(),
                                url,
                                token,
                            )
                            logging.info('\t\t----------------------- MESSAGE CHANGE STATUS IN DB ---------------------')
                            await change_status(message_in_db.id, 'sended')
                        else:
                            # its too late to send message
                            logging.info('\t\t----------------------- WINDOW IS BROKEN  ---------------------')
                            logging.info('\t\t----------------------- MESSAGE LOST ---------------------')
                            continue
                    else:
                        await send_message(
                            MessageRequest(
                                id=message_in_db.id,
                                phone=message.phone,
                                text=mailing_task.body
                            ).dict(),
                            url,
                            token,
                        )
                else:
                    # it's to early to send message
                    message_queue.append(message)
                    logging.info('\t\t----------------------- MESSAGE IS SHIFTED TO TOP ---------------------')
                    await asyncio.sleep(0.001)
            except BadResponse as e:
                # something wrong with reciever
                logging.warning(e.__str__())
            except HTTPException as e:
                logging.warning(e.detail())
            except Exception as e:
                # something wrong with the code
                logging.warning(e.__str__())
