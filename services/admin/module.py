import logging
import secrets

from sqlalchemy import delete, exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.esp import Esp
from services.auth.hash import hash_token

logger = logging.getLogger(__name__)


class InteractionWithModule:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    async def generate_api_key():
        return secrets.token_urlsafe(32)

    async def create_module(self):
        try:
            api_key = await self.generate_api_key()
            hash_api_key = hash_token(api_key)
            new_module = Esp(hashed_api_key=hash_api_key, lat=0.0, lon=0.0)

            self.session.add(new_module)
            await self.session.commit()

            await self.session.refresh(new_module)

            return {"id": new_module.id, "api": api_key}
        except Exception as e:
            await self.session.rollback()
            logger.critical(f"Ошибка при попытке создания модуля{e}")
            raise

    async def delete_module(self, esp_id: int):
        try:
            delete_device = delete(Esp).where(Esp.id == esp_id)
            await self.session.execute(delete_device)
            await self.session.commit()
            return {"message": "Модуль удален"}

        except exc.SQLAlchemyError as e:
            logger.critical(f"Ошибка при удалении модуля {esp_id}. Error: {e}")
            raise

    async def get_modules(self):

        try:
            get = select(Esp)
            result = await self.session.execute(get)
            modules = result.scalars().all()
            return modules
        except exc.SQLAlchemyError as e:
            logger.error(f"Ошибка при получении модулей: {e}")
            raise
