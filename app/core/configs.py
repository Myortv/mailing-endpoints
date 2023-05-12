from typing import Any, Dict, List, Optional

from fastapi_auth0 import Auth0

from pydantic import BaseSettings, AnyHttpUrl, validator

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.controllers import fetch_timezones


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Mailer"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost"]
    DOCS_URL: str = '/docs'

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    OAUTHDOMAIN: str
    OAUTHAUDIENCE: str
    AUTH: Auth0 = None

    # TZ_NAMES: frozenset = None
    # TZ_ABBREV: frozenset = None
    # TZ_OFFSET: frozenset = None
    TZ_POSTGRES: frozenset = None

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls,
        v: str | List[str]
    ) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    async def fetch_timezones(self):
        # self.TZ_NAMES, self.TZ_ABBREV, self.TZ_OFFSET = await fetch_timezones()
        self.TZ_POSTGRES = await fetch_timezones()


tags_metadata = [
    {
        "name": "Mailing",
         "description": "Manage Mailing<br>"
            "Mailings uses for scheduling messsaging. You can set any start "
            "or end time points and filters. Filters uses exists clients "
            "properties, so you can add, one, two, or not add filters at all",
    },
    {
        "name": "Client",
        "description": "Manage Clients.<br>"
            "Clients represents the phone number owner."
            "Clients have mailing window in what they will recieve messages<br>"
            "For example if start_recieve for client setted at 12:00, so client "
            "will recieve message starting that time (of course in his "
            "local timezone)<br>"
            "Clients make window with 'start_at' and 'duration'. "
            "Duration uses to represent an cycling window. "
            "for exampe if user start recieving at 22:00, so with duration of "
            "5hr, they will end recieving at 3:00 next day. "
            "Duration setted in seconds",
    },
]

settings = Settings()
