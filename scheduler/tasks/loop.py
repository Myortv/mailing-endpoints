from fastapi import HTTPException

from typing import List

import aiohttp

from datetime import datetime, timedelta

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

from pydantic import ValidationError

from scheduler.exceptions.exceptions import BadResponse

import logging


async def mailing_task(
    mailing_task: Mailing,
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
                        )
                else:
                    # it's to early to send message
                    logging.info(f'\t\t----------------------- {message} ---------------------')
                    logging.info('\t\t----------------------- MESSAGE IS SHIFTED TO TOP ---------------------')
                    message_queue.append(message)
                    if id(message) == id(message_queue[0]):
                        logging.info('\t\t----------------------- NO MESSAGE CAN BE SERVED ---------------------')
                        mailing_task.timeout = datetime.now() + timedelta(seconds=10)
                        logging.info('\t\t----------------------- TIMEOUT JOB FOR 10 SEC ---------------------')
                        break
            except ValidationError as e:
                logging.info('\t\t----------------------- VALIDATION ERROR ---------------------')
                logging.warning(e.__str__())
            except BadResponse as e:
                # something wrong with reciever
                logging.info(f'\t\t----------------------- BAD RESPONSE ({e.response.status}) ---------------------')
                logging.warning(e.__str__())
                logging.warning(await e.response.text())
            except HTTPException as e:
                logging.info('\t\t----------------------- HTTPEXCEPTION ERROR ---------------------')
                logging.warning(e.detail())
            except Exception as e:
                # something wrong with the code
                logging.info('\t\t----------------------- COMMON EXCEPTION ERROR ---------------------')
                logging.warning(e.__str__())
