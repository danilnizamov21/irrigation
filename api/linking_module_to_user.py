from authx import TokenPayload
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import auth
from core.db import get_session
from schemas.esp import EspResponse, EspUpdate
from services.linking_module_to_user import LinkinModule

router = APIRouter()


async def get_linking_service(db: AsyncSession = Depends(get_session)) -> LinkinModule:
    """Зависимость дял получения сервиса LinkinMoudle"""
    return LinkinModule(db)


@router.post("/link_module")
async def link_module(
    module_key: str,
    token: TokenPayload = Depends(auth.access_token_required),
    service: LinkinModule = Depends(get_linking_service),
):
    """Роутер для того чтобы привязать модуль к юзеру"""

    user_id = int(token.sub)
    linking = await service.linking_module_to_user(module_key, user_id)
    # по апи ключу найти модуль в бд
    # в линкинг таблицу записать айди модуля и айди юзера
    return linking


@router.get("/get_all_modules")
async def get_all_model(
    token: TokenPayload = Depends(auth.access_token_required),
    service: LinkinModule = Depends(get_linking_service),
):
    """Получение всех id модулей у юзера"""

    user_id = int(token.sub)
    return await service.get_user_modules(user_id=user_id)


@router.get("/get_one_module", response_model=EspResponse)
async def get_one_module(
    esp_id: int,
    token: TokenPayload = Depends(auth.access_token_required),
    service: LinkinModule = Depends(get_linking_service),
):
    """Получние информации по одному модулю"""

    return await service.get_module(esp_id)


@router.patch("/update_module_data")
async def update_module(
    esp_id: int,
    payload: EspUpdate,
    token: TokenPayload = Depends(auth.access_token_required),
    service: LinkinModule = Depends(get_linking_service),
):
    """Обновление данных модуля"""

    return await service.update_module(esp_id, payload)
