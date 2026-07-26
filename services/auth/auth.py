import logging
from datetime import timedelta
from typing import Any

from authx import AuthX, AuthXConfig
from fastapi import HTTPException
from redis import RedisError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.user import UserLogin, UserRegister
from services.auth.hash import hash_pass, hash_token, verify_password

config = AuthXConfig()
config = AuthXConfig(
    JWT_SECRET_KEY="your-secret-keyq0w9odkq9e02di2093owdke9033iedo902de209",
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=15),  # Short-lived
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30),  # Long-lived
)


auth = AuthX(config=config)

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, session: AsyncSession, redis_con):
        self.session = session
        self.redis_con = redis_con

    async def get_user_by_login(self, login: str) -> User | None:
        """Получение юзера по логину"""
        try:
            select_ = select(User).where(User.login == login)
            result = await self.session.execute(select_)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.critical(
                f"Возникла ошибка при обращение к бд с данными {login}.Ошибка: {e}"
            )
            raise

    async def register_user(self, payload: UserRegister) -> Any:
        """Регистрация пользователя"""
        try:
            check_login = await self.get_user_by_login(payload.login)

            if check_login is not None:
                raise HTTPException(status_code=400, detail="Логин уже занят")

            hsh_pwd = hash_pass(payload.password)

            new_user = User(
                login=payload.login,
                email=payload.email,
                hash_password=hsh_pwd,
            )

            self.session.add(new_user)
            await self.session.commit()

            await self.session.refresh(new_user)

            return {"message": "Вы успешно зарегистрировались"}
        except Exception as e:
            await self.session.rollback()
            logger.critical(
                f"Ошибка при попытке регистрации {e}. Данные login={payload.login}"
            )
            raise

    async def authenticate_user(self, payload: UserLogin) -> dict[str, str]:
        """Авторизация пользователя"""
        try:
            check_login = await self.get_user_by_login(payload.login)
            if check_login is None:
                raise HTTPException(status_code=400, detail="Логин не найден")
            if verify_password(payload.password, check_login.hash_password) is False:
                raise HTTPException(status_code=400, detail="Неверный логин или пароль")

            access_token = auth.create_access_token(uid=str(check_login.id))
            refresh_token = auth.create_refresh_token(uid=str(check_login.id))
            await self.save_refresh_token(refresh_token, check_login.id)

            return {"access_token": access_token, "refresh_token": refresh_token}
        except Exception as e:
            logger.critical(
                f"Ошибка при попытке авторизации {e}. Данные login={payload.login}"
            )
            raise

    async def save_refresh_token(self, token: str, user_id: int) -> str | None:
        "Хэшируем токен и передаем в бд редис"
        try:
            hashed_token = hash_token(token)
            r = await self.redis_con
            await r.set(f"hashed_token:{hashed_token}", user_id, ex=2419000)
        except RedisError:
            logger.critical(
                f"Ошибка при попытке сохранении токена в Редис user_id={user_id}"
            )
            raise

    async def refresh_access_token(self, token: str, sub: str) -> str:
        """Проверка хеша и выдача нового access токена"""

        hashed_token = hash_token(token)

        try:
            check = await self.redis_con.get(f"hashed_token:{hashed_token}")
        except RedisError:
            logger.exception(
                f"Ошибка Redis при обновлении access_token для user_id={sub}"
            )
            raise

        if not check:
            raise HTTPException(
                status_code=401,
                detail="Недействительный или истекший refresh токен",
            )

        access_token = auth.create_access_token(uid=str(sub))
        return access_token
