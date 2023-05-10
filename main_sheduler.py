import pytz

import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.triggers.interval import IntervalTrigger

from scheduler.db.base import DatabaseManager

from scheduler.core.configs import settings

from scheduler.jobs.jobs import check_free_mailing, clean_tasks

import logging
import datetime


logging.basicConfig(level=logging.INFO)

DEFAULT_TIMEZONE = datetime.datetime.now().tzinfo

scheduler = AsyncIOScheduler()

settings.SCHEDULER = scheduler
# trigger = IntervalTrigger(minutes=3)
trigger_check_free = IntervalTrigger(seconds=2)
trigger_clean_tasks = IntervalTrigger(seconds=2)


scheduler.configure(
    jobstores={'default': MemoryJobStore()},
    executors={'default': AsyncIOExecutor()},
    timezone=DEFAULT_TIMEZONE,
)

async def shutdown():
    logging.info('\t\t----------------------- SHUTTING DOWN ---------------------')
    await DatabaseManager.stop()

async def startup():
    logging.info('\t\t----------------------- START  STARTUP ---------------------')
    await DatabaseManager.start(
        settings.POSTGRES_DB,
        settings.POSTGRES_USER,
        settings.POSTGRES_PASSWORD,
        settings.POSTGRES_HOST,
    )
    logging.info('\t\t----------------------- START  SCHEDULER ---------------------')
    # await scheduler.start_in_background()
    scheduler.start()
    logging.info('\t\t----------------------- ADD JOB ---------------------')
    scheduler.add_job(check_free_mailing, trigger_check_free, max_instances=1)
    scheduler.add_job(clean_tasks, trigger_clean_tasks, max_instances=1)
    logging.info('\t\t----------------------- END  STARTUP ---------------------')

if __name__== '__main__':

    try:
        asyncio.get_event_loop().run_until_complete(startup())
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        logging.info('\tP\t----------------------- INTERRUPTED ---------------------')
        asyncio.get_event_loop().run_until_complete(shutdown())
        import sys
        sys.exit()
    except Exception as e:
        logging.info('\tP\t----------------------- INTERRUPTED ---------------------')
        asyncio.get_event_loop().run_until_complete(shutdown())
        raise e
