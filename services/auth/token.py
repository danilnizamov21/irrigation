import logging

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from models.user import User
from schemas.user import UserRegister
from services.auth.hash import hash_pass


class Tokens:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_user_by_login(self, login: str) -> User | None:
        try:
            select_ = select(User).where(User.login == login)
            result = await self.session.execute(select_)
            return result.scalar_one_or_none()
        except Exception as e:
            logging.critical(
                f"Возникла ошибка при обращение к бд с данными {login}.Ошибка: {e}"
            )
            raise e

    async def register(self, payload: UserRegister):

        check_login = await self.get_user_by_login(payload.login)
        hsh_pwd = await hash_pass(payload.password)

        if check_login is not None:
            raise HTTPException(status_code=400, detail="Логин уже занят")
        try:
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
            self.session.rollback()
            logging.critical(
                f"Ошибка при попытке регистрации {e}", f"Данные login={payload.login}"
            )
            raise e
