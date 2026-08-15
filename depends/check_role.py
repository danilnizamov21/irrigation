from typing import Annotated

from authx import TokenPayload
from fastapi import Depends, HTTPException

from api.auth import AuthServiceDep, auth
from models.user import User


async def get_current_user(
    service: AuthServiceDep, token: TokenPayload = Depends(auth.access_token_required)
) -> User:
    user = await service.user_me(int(token.sub))
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


async def get_current_user_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.role == "super":
        raise HTTPException(
            status_code=403, detail="Доступ запрещен. Требуются права администратора"
        )
    return current_user


AdminUserDep = Annotated[User, Depends(get_current_user_admin)]
