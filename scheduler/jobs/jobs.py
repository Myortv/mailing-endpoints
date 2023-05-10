from typing import List

import asyncio

from scheduler.schemas.mailing import MailingInDB
from scheduler.schemas.client import ClientInDB

# from app.db.base import DatabaseManager
from scheduler.controllers.mailing import get_nearest_mailing
from scheduler.controllers.client import get_free_clients

from scheduler.core.alive import AliveMailings
from scheduler.schemas.datatypes import Mailing

from scheduler.tasks.loop import mailing_task

from datetime import datetime, timedelta

import logging

logging.basicConfig(level=logging.INFO)



async def check_free_mailing():
    logging.info(f'\t\t----------------------- START SPAWNING JOB -----------------------')
    mailings: List[MailingInDB] = await get_nearest_mailing()
    logging.info(f'\t\tstart serving mailings. Taken mailings: \n{mailings}')
    for mailing in mailings:
        logging.info(f'\t\tinside for loop. {mailing.id}')
        if not AliveMailings.mailings.get(mailing.id):
            logging.info(f'\t\tinside check_free_mailing. {mailing.id}')
            logging.info(f'\t\t----------------------- START MAILING TASK CREATION -----------------------')
            # mailing is not still started, create task
            logging.info(f'\t\tinside check_free_mailing. {mailing.id} start creating mailing task holder')
            mailing_task_holder = Mailing(
                id=mailing.id,
                start_at=mailing.start_time,
                end_at=mailing.end_time,
                body=mailing.body,
            )
            logging.info(f'\t\tcreated mailing_task_holder {mailing_task_holder}')
            logging.info(f'\t\tinside check_free_mailing. {mailing.id} mailing task creation')
            clients: List[ClientInDB] = await get_free_clients(
                mailing.id,
                mailing.return_filter()
            )
            logging.info(f'\t\tTaken clients \n{clients}')
            AliveMailings.mailings[mailing.id] = mailing_task_holder
            logging.info(f'\t\tAliveMailings updated {AliveMailings.mailings}')
            if clients:
                # mailing has some clients to process
                logging.info(f'\t\tinside check_free_mailing. {mailing.id} mailing task creation')
                mailing_task_holder.set_message_queue(clients)
                logging.info(f'\t\tmessages generated {mailing_task_holder.message_queue}')
                mailing_task_holder.task = asyncio.create_task(
                    mailing_task(
                        mailing_task_holder
                    )
                )
                logging.info(f'\t\tinside check_free_mailing. {mailing.id} mailing task created')
                logging.info(f'\t\tinside check_free_mailing. {mailing.id}')
                logging.info(f'\t\t----------------------- MAILING TASK CREATED -----------------------')
                logging.info(f'\t\t----------------------- END MAILING TASK CREATION -----------------------')
                logging.info(f'\t\t----------------------- END ITERATION -----------------------')
                continue
            else:
                # new mailing created but no clients exists
                # set timeout for task
                logging.info(f'\t\tinside check_free_mailing. {mailing.id}')
                logging.info(f'\t\tmailing is suspended for 1 minuts')
                # mailing_task_holder.timeout = datetime.now() + timedelta(minutes=1)
                mailing_task_holder.timeout = datetime.now() + timedelta(seconds=15)
                AliveMailings.mailings[mailing.id] = mailing_task_holder
                logging.info(f'\t\t----------------------- MAILING SUSPENDED -----------------------')
                logging.info(f'\t\t----------------------- END ITERATION -----------------------')
                continue
    logging.info(f'\t\t----------------------- END SPAWNING JOB -----------------------')


async def clean_tasks():
    logging.info(f'\t\t----------------------- START CLEANING JOB -----------------------')
    mailings = AliveMailings.mailings.copy()
    logging.info(f'\t\tstart serving mailings. Alive mailings: \n{mailings}')
    for key in mailings:
        logging.info(f'\t\t----------------------- START PROCESSING EXISTING TASK -----------------------')
        mailing_task_holder: Mailing = mailings[key]
        logging.info(f'\t\tinside check_free_mailing. {mailing_task_holder.id}')
        logging.info(f'\t\tmailing task holder taken')
        if mailing_task_holder.timeout:
            logging.info(f'\t\tmailing task has timeout')
            if datetime.now() > mailing_task_holder.timeout:
                # time out has passed, close task to create new one in next iteration
                if not mailing_task_holder.task:
                    AliveMailings.mailings.pop(mailing_task_holder.id)
                    logging.info(f'\t\t----------------------- TASK NEVER STARTED -----------------------')
                    logging.info(f'\t\t----------------------- CLEAN TASK -----------------------')
                    logging.info(f'\t\t----------------------- END ITERATION -----------------------')
                    continue
                logging.info(f'\t\tmailing task has timed out')
                mailing_task_holder.task.cancel()
                logging.info(f'\t\tmailing task cancaled')
            else:
                logging.info(f'\t\t----------------------- TASK SUSPENDED -----------------------')
                logging.info(f'\t\t----------------------- END ITERATION -----------------------')
                continue
        if mailing_task_holder.task.done():
            logging.info(f'\t\tmailing task has been done')
            if e := mailing_task_holder.task.exception():
                logging.info(f'\t\tmailing task has been ended with exception')
                logging.warning(e.__str__())
            AliveMailings.mailings.pop(mailing_task_holder.id)
            logging.info(f'\t\tmailing task has been ended. AliveMailings cleaned')
            logging.info(f'\t\t----------------------- END EXSISTING TASK -----------------------')
            logging.info(f'\t\t----------------------- END ITERATION -----------------------')
            continue
    logging.info(f'\t\t----------------------- END ITERATION -----------------------')
    logging.info(f'\t\t----------------------- END CLEANING JOB -----------------------')
