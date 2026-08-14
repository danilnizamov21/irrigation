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


@router.get("/modules")
async def get_all_model(
    token: TokenPayload = Depends(auth.access_token_required),
    service: LinkinModule = Depends(get_linking_service),
):
    """Получение всех id модулей у юзера"""

    user_id = int(token.sub)
    return await service.get_user_modules(user_id=user_id)


@router.get("/module/{module_key}", response_model=EspResponse)
async def get_one_module(
    module_key: int,
    token: TokenPayload = Depends(auth.access_token_required),
    service: LinkinModule = Depends(get_linking_service),
):
    """Получние информации по одному модулю"""

    return await service.get_module(module_key)


@router.patch("/module/{module_key}")
async def update_module(
    module_key: int,
    payload: EspUpdate,
    token: TokenPayload = Depends(auth.access_token_required),
    service: LinkinModule = Depends(get_linking_service),
):
    """Обновление данных модуля"""

    return await service.update_module(module_key, payload)


@router.delete("/{module_id}")
async def delete_module(
    module_id: int,
    token: TokenPayload = Depends(auth.access_token_required),
    service: LinkinModule = Depends(get_linking_service),
):
    """Удаление модуля из списка модулей юзера"""
    return await service.delete_module(module_id, int(token.sub))


@router.get("/story/{module_id}")
async def get_irrigation_story(
    module_id: int,
    token: TokenPayload = Depends(auth.access_token_required),
    service: LinkinModule = Depends(get_linking_service),
):
    """Получение истории полива конкретного модуля"""
    return await service.get_irrigation_story(module_id)
