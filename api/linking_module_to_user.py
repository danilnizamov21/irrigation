from authx import TokenPayload
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import auth
from core.db import get_session
from schemas.esp import EspResponse
from services.linking_module_to_user import LinkinModule

router = APIRouter()


@router.post("/link_module")
async def link_module(
    module_key: str,
    token: TokenPayload = Depends(auth.access_token_required),
    db: AsyncSession = Depends(get_session),
):
    """Роутер для того чтобы привязать модуль к юзеру"""
    linking_cls = LinkinModule
    user_id = int(token.sub)
    linking = await linking_cls.linking_module_to_user(module_key, user_id, db)
    # по апи ключу найти модуль в бд
    # в линкинг таблицу записать айди модуля и айди юзера
    return linking


@router.get("/get_all_modules")
async def get_all_model(
    token: TokenPayload = Depends(auth.access_token_required),
    db: AsyncSession = Depends(get_session),
):
    linking_cls = LinkinModule
    return await linking_cls.get_user_modules(int(token.sub), db)


@router.get("/get_one_module", response_model=EspResponse)
async def get_one_module(
    esp_id: int,
    token: TokenPayload = Depends(auth.access_token_required),
    db: AsyncSession = Depends(get_session),
):
    linking_cls = LinkinModule
    return await linking_cls.get_module(esp_id, db)
