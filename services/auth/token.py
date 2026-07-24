import logging
from datetime import timedelta

from authx import AuthX, AuthXConfig
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from models.user import User
from schemas.user import UserLogin, UserRegister
from services.auth.hash import hash_pass, verify_password

config = AuthXConfig()
config = AuthXConfig(
    JWT_SECRET_KEY="your-secret-keyq0w9odkq9e02di2093owdke9033iedo902de209",
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=15),  # Short-lived
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30),  # Long-lived
)


auth = AuthX(config=config)


class AuthService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_user_by_login(self, login: str) -> User | None:
        """Получение юзера по логину"""
        try:
            select_ = select(User).where(User.login == login)
            result = await self.session.execute(select_)
            return result.scalar_one_or_none()
        except Exception as e:
            logging.critical(
                f"Возникла ошибка при обращение к бд с данными {login}.Ошибка: {e}"
            )
            raise e

    async def register_user(self, payload: UserRegister):
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
            logging.critical(
                f"Ошибка при попытке регистрации {e}. Данные login={payload.login}"
            )
            raise e

    async def authenticate_user(self, payload: UserLogin):
        """Авторизация пользователя"""
        try:
            check_login = await self.get_user_by_login(payload.login)
            if check_login is None:
                raise HTTPException(status_code=400, detail="Логин не найден")
            if verify_password(payload.password, check_login.hash_password) is False:
                raise HTTPException(status_code=400, detail="Неверный логин или пароль")

            access_token = auth.create_access_token(uid=str(check_login.id))
            refresh_token = auth.create_refresh_token(uid=str(check_login.id))

            return {"access_token": access_token, "refresh_token": refresh_token}
        except Exception as e:
            logging.critical(
                f"Ошибка при попытке авторизации {e}. Данные login={payload.login}"
            )
            raise
