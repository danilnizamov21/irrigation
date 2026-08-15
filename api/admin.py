from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from depends.check_role import AdminUserDep
from schemas.esp import EspCreateResponse
from services.admin.module import InteractionWithModule

router = APIRouter()


async def get_interaction_service(
    db: AsyncSession = Depends(get_session),
) -> InteractionWithModule:
    """Зависимость дял получения сервиса InteractionWithModule"""
    return InteractionWithModule(db)


@router.post("/module", response_model=EspCreateResponse)
async def create_module(
    admin: AdminUserDep,
    service: InteractionWithModule = Depends(get_interaction_service),
):
    result = await service.create_module()
    return result


@router.delete("/module{id}")
async def delete_module_by_id(
    admin: AdminUserDep,
    esp_id: int,
    service: InteractionWithModule = Depends(get_interaction_service),
):
    return await service.delete_module(esp_id=esp_id)


@router.get("/modules")
async def get_modules(
    admin: AdminUserDep,
    service: InteractionWithModule = Depends(get_interaction_service),
):
    return await service.get_modules()
