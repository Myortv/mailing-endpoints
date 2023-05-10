from typing import Any, Dict, List, Optional

from fastapi_auth0 import Auth0

from pydantic import BaseSettings, AnyHttpUrl, validator

from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Mailer"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost"]
    DOCS_URL: str = 'docs'

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    OAUTHDOMAIN: str
    OAUTHAUDIENCE: str
    AUTH: Auth0 = None

    SCHEDULER: AsyncIOScheduler = None

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


settings = Settings()
