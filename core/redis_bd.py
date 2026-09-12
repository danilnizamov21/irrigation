import logging
import os

import redis.asyncio as asyncred
from dotenv import find_dotenv, load_dotenv

logger = logging.getLogger(__name__)

file_loaded = load_dotenv(find_dotenv(), verbose=True, override=False)

pwd = os.getenv("REDIS_PWD")
host = os.getenv("REDIS_HOST", "redis")
port = os.getenv("REDIS_PORT", 6379)

_redis_client: asyncred.Redis | None = None


async def init_redis() -> asyncred.Redis:
    global _redis_client
    try:
        _redis_client = asyncred.Redis(
            host=host,
            port=int(port),
            decode_responses=True,
            username="default",
            password=pwd,
        )
        await _redis_client.ping()
        logger.info("Успешное подключение к редис")
        return _redis_client
    except asyncred.RedisError as a:
        logger.critical(f"Ошибка при подключении к редис: {a}")
        raise


async def close_redis() -> None:
    global _redis_client
    if _redis_client is not None:
        await _redis_client.aclose()
        _redis_client = None


def get_redis() -> asyncred.Redis:
    if _redis_client is None:
        raise RuntimeError("Redis-клиент не инициализирован")
    return _redis_client
