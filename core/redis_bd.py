import logging
import os

import redis.asyncio as asyncred
from dotenv import find_dotenv, load_dotenv

logger = logging.getLogger(__name__)

file_loaded = load_dotenv(find_dotenv(), verbose=True, override=True)

pwd = os.getenv("REDIS_PWD")
host = os.getenv("REDIS_HOST", "redis")
port = os.getenv("REDIS_PORT", 6379)


async def connect_to_redis():
    try:
        redis_connect = asyncred.Redis(
            host=host,
            port=int(port),
            decode_responses=True,
            username="default",
            password=pwd,
        )

        await redis_connect.ping()
        logger.info("Успешное подключение к редис")

        return redis_connect
    except asyncred.RedisError as a:
        logger.critical(f"Ошибка при подключении к редис: {a}")
        raise
