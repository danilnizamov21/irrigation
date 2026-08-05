from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from schemas.esp import SoilData
from services.check_api_key import get_device_by_key
from services.irrigation_and_weather.irrigation_decision_for_today import (
    get_irrigation_decision_for_today,
)

router = APIRouter()


@router.post("/telemetry")
async def telemetry(payload: SoilData, db: AsyncSession = Depends(get_session)):
    """Метод получает телеметрию и отдает ответ о поливе"""
    device = await get_device_by_key(payload.api_key, db)
    decision = await get_irrigation_decision_for_today(
        lat=device.lat, lon=device.lon, soil_moisture=payload.moisture
    )
    return decision
