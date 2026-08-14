from authx import TokenPayload
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import auth
from core.db import get_session
from schemas.esp import SoilData
from services.check_api_key import get_device_by_key
from services.irrigation_and_weather.irrigation_decision_for_today import (
    get_irrigation_decision_for_today,
)
from services.irrigation_and_weather.recording_result import recording_irrigation_resul

router = APIRouter()


@router.post("/telemetry")
async def telemetry(payload: SoilData, db: AsyncSession = Depends(get_session)):
    """Метод получает телеметрию и отдает ответ о поливе"""
    device = await get_device_by_key(payload.api_key, db)
    decision = await get_irrigation_decision_for_today(
        lat=device.lat, lon=device.lon, soil_moisture=payload.moisture
    )
    await recording_irrigation_resul(device.id, decision, db)
    return decision


@router.post("/start")
async def start(esp_: int, duration: int):
    # TODO ручка тестовая, требует реализации уже в будущем. Через HTTP запрос будет поступать на есп32 и включать полив на определенный промежуток времени.Своего рода ручное управление
    # TODO так же стоит реализовать ручку полной остановки автополива.
    pass


@router.post("/stop")
async def stop(esp: int):
    pass


@router.get("/telemetry")
async def get_telemetry(
    esp_id, token: TokenPayload = Depends(auth.access_token_required)
):
    # TODO ручка должна принимать id делать запрос к модулю и получать данные от него.
    pass
