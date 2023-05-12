from fastapi import HTTPException

from pydantic import ValidationError, BaseModel

import asyncpg

import logging

from app.utils.exceptions import raise_exception


class DatabaseManager:
    POOL: asyncpg.Pool = None

    @classmethod
    async def start(
        cls,
        database: str,
        user: str,
        password: str,
        host: str,
    ) -> None:
        cls.POOL = await asyncpg.create_pool(
            database=database,
            user=user,
            password=password,
            host=host,
        )
        logging.info(f'DatabaseManager create postgres pool on:{cls.POOL}')

    @classmethod
    async def stop(cls):
        await cls.POOL.close()
        logging.info(f'DatabaseManager stops postgres pool on:{cls.POOL}')



    @classmethod
    def acquire_connection(cls):
        def decorator(func):
            async def wrapper(*args, **kwargs):
                async with cls.POOL.acquire() as conn:
                    try:
                        result = await func(*args, conn=conn, **kwargs)
                        return result
                    except ValidationError as e:
                        raise_exception(e)
                    except HTTPException as e:
                        raise_exception(e)
                    except Exception as e:
                        logging.warning(e)
            return wrapper
        return decorator


def unpack_data(data):
    if isinstance(data, dict):
        fields = list(data.keys())
        values = list(data.values())
        return fields, values
    fields = list(data.__dict__.keys())
    values = list(data.__dict__.values())
    assert len(fields) == len(values)
    return (fields, values)


def generate_placeholder(data, i=0):
    pair = []
    values_out = []
    fields, values = unpack_data(data)
    for j, field in enumerate(fields):
        if values[j] is not None:
            i += 1
            pair.append(f' {field} = ${i} ')
            values_out.append(values[j])
    return pair, values_out

