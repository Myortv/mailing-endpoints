import pytz

import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor

from app.db.base import DatabaseManager

from app.core.configs import settings

DEFAULT_TIMEZONE = pytz.utc


scheduler = AsyncIOScheduler()

settings.SCHEDULER = scheduler

from app.sheduler.jobs import (
    some_func
)

scheduler.configure(
    jobstores={'default': MemoryJobStore()},
    executors={'default': AsyncIOExecutor()},
    job_defaults={'coalesce': False, 'max_instatnces': 1},
    timezone=DEFAULT_TIMEZONE,
)

async def shutdown():
    await DatabaseManager.stop()

async def startup():
    await DatabaseManager.start(
        settings.POSTGRES_DB,
        settings.POSTGRES_USER,
        settings.POSTGRES_PASSWORD,
        settings.POSTGRES_HOST,
    )


if __name__== '__main__':
    scheduler.start()

    async def placeholder():
        while True:
            await asyncio.sleep(0.1)
    asyncio.get_event_loop().run_until_complete(startup())

    try:
        asyncio.get_event_loop().run_forever()
    except Exception as e:
        asyncio.get_event_loop().run_until_complete(shutdown())
        raise e
