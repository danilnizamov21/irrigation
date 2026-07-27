from fastapi import APIRouter, Depends

from models.esp import Esp
from schemas.esp import SoilData
from services.check_api_key import get_device_by_key
from services.irrigation_and_weather.irrigation_decision_for_today import (
    get_irrigation_decision_for_today,
)

router = APIRouter()


@router.post("/telemetry")
async def telemetry(payload: SoilData, device: Esp = Depends(get_device_by_key)):
    """Метод получает телеметрию и отдает ответ о поливе"""
    decision = await get_irrigation_decision_for_today(
        lat=device.lat, lon=device.lon, soil_moisture=payload.moisture
    )
    return decision
