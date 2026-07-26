from datetime import timedelta
from typing import Annotated

from authx import AuthX, AuthXConfig
from fastapi import APIRouter, Depends, Request, Response
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from core.redis_bd import connect_to_redis
from schemas.user import UserLogin, UserRegister
from services.auth.auth import AuthService

router = APIRouter()
config = AuthXConfig()
config = AuthXConfig(
    JWT_SECRET_KEY="your-secret-keyq0w9odkq9e02di2093owdke9033iedo902de209",
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=15),  # Short-lived
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30),  # Long-lived
)


auth = AuthX(config=config)


async def get_auth_service(
    session: AsyncSession = Depends(get_session),
    redis_con: Redis = Depends(connect_to_redis),
) -> AuthService:
    return AuthService(session=session, redis_con=redis_con)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


@router.post("/login")
async def login(payload: UserLogin, response: Response, service: AuthServiceDep):
    tokens = await service.authenticate_user(payload)
    refresh_token = tokens["refresh_token"]
    auth.set_refresh_cookies(refresh_token, response, max_age=2419200)
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
    }


@router.post("/register")
async def register(payload: UserRegister, service: AuthServiceDep):
    return await service.register_user(payload)


@router.post("/refresh")
async def refresh(
    service: AuthServiceDep,
    request: Request,
):
    cookie = request.cookies
    access_token = await service.refresh_access_token(cookie["refresh_token_cookie"])
    print(f"TOKEN: {cookie['refresh_token_cookie']}")
    return {"access_token": access_token}


@router.get("/protected", dependencies=[Depends(auth.access_token_required)])
async def protected():
    return {"message": "Hello World"}


@router.post("/logout")
async def logout(service: AuthServiceDep, response: Response, request: Request):
    cookie = request.cookies
    await service.delete_refresh_token(cookie["refresh_token_cookie"])
    auth.unset_cookies(response)

    return {"message": "Успешный выход из системы"}
