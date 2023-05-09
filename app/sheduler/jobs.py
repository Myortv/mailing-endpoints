from app.core.configs import settings
from random import randint
import asyncio

from apscheduler.triggers.interval import IntervalTrigger

trigger = IntervalTrigger(minutes=1)


async def shedule_mailing():



settings.SCHEDULER.add_job(
    some_func,
    trigger=trigger,
)
