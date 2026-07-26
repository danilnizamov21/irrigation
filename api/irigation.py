from fastapi import APIRouter

from services.irrigation_and_weather.irrigation_decision_for_today import (
    get_irrigation_decision_for_today,
)

router = APIRouter()


@router.post("/telemetry")
async def telemetry(lat: float, lon: float, soil_moisture: int):
    return await get_irrigation_decision_for_today(lat, lon, soil_moisture)
