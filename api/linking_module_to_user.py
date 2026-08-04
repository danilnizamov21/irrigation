from authx import TokenPayload
from fastapi import APIRouter, Depends

from api.auth import auth

router = APIRouter()


@router.post("/link_module")
async def link_module(
    module_key: str, token: TokenPayload = Depends(auth.refresh_token_required)
):
    user_id = int(token.sub)

    # по апи ключу найти модуль в бд
    # в линкинг таблицу записать айди модуля и айди юзера
    return user_id
