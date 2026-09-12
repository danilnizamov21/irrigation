import os
from urllib.parse import quote_plus

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(), override=False)


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Не задана переменная окружения {name}")
    return value


POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PWD = _require("POSTGRES_PWD")
POSTGRES_NAME = _require("POSTGRES_NAME")
POSTGRES_HOST = _require("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")


def jwt_secret_key() -> str:
    return _require("JWT_SECRET_KEY")


def async_database_url() -> str:
    user = quote_plus(POSTGRES_USER)
    password = quote_plus(POSTGRES_PWD)
    return (
        f"postgresql+asyncpg://{user}:{password}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"
    )


def alembic_database_url() -> str:
    return async_database_url() + "?async_fallback=True"
