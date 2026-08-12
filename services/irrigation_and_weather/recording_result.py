import logging

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models.irrigation import SoilMeasurements

logger = logging.getLogger(__name__)


async def recording_irrigation_resul(
    esp_id: int, irrigation: str, db: AsyncSession
) -> None:
    try:
        new_record = SoilMeasurements(esp_id=esp_id, irrigation=irrigation)
        db.add(new_record)
        await db.commit()

    except SQLAlchemyError as e:
        await db.rollback()
        logger.critical(f"Ошибка бд: {e}")

        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка базы данных",
        )
