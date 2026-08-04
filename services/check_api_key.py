import logging

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import (
    SQLAlchemyError,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from models.esp import Esp
from schemas.esp import SoilData
from services.auth.hash import hash_token

logger = logging.getLogger(__name__)


async def get_device_by_key(
    payload: SoilData | str, db: AsyncSession = Depends(get_session)
) -> Esp:
    try:
        if payload is SoilData:
            hashed = hash_token(payload.api_key)
        else:
            hashed = hash_token(payload)
        # esp_12eo120w12wl0121ws

        query = select(Esp).where(Esp.hashed_api_key == hashed)
        result = await db.execute(query)
        device = result.scalar_one_or_none()

        if not device:
            raise HTTPException(
                status_code=401,
                detail="Не существует такого API ключа",
            )

        return device
    except SQLAlchemyError as e:
        logger.critical(f"Ошибка бд: {e}")

        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка базы данных",
        )
