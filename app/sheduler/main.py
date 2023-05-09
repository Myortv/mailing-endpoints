import pytz

import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor

from .db.base import DatabaseManager

from .core.configs import settings

DEFAULT_TIMEZONE = pytz.utc


scheduler = AsyncIOScheduler()

scheduler.configure(
    jobstores={'default': MemoryJobStore()},
    executors={'default': AsyncIOExecutor()},
    job_defaults={'coalesce': False, 'max_instatnces': 1},
    timezone=DEFAULT_TIMEZONE,
)

if __name__== '__main__':
    asyncio.run(DatabaseManager.start(
        settings.POSTGRES_DB,
        settings.POSTGRES_USER,
        settings.POSTGRES_PASSWORD,
        settings.POSTGRES_HOST,
    ))

    settings.SCHEDULER = scheduler

    scheduler.start()

from .sheduler.jobs import (
    some_func
)
