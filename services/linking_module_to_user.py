import logging

from sqlalchemy import delete, exc, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.esp import Esp
from models.irrigation import SoilMeasurements
from models.user_esp import user_esp_association
from schemas.esp import EspUpdate
from services.auth.hash import hash_token
from services.check_api_key import get_device_by_key

logger = logging.getLogger(__name__)


class LinkinModule:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def linking_module_to_user(self, key: str, user_id: int) -> bool:
        """Привязка модуля к пользователю"""
        try:
            device = await get_device_by_key(key, self.session)
            linking = insert(user_esp_association).values(
                user_id=user_id, esp_id=device.id
            )
            await self.session.execute(linking)
            await self.session.commit()
            return True
        except exc.SQLAlchemyError as e:
            await self.session.rollback()
            logger.critical(f"Ошибка при попытке связать модуль с юзером: {e}")
            raise

    async def get_user_modules(self, user_id: int):
        """Получениие всех модулей юзера. Возвращаются ID"""
        try:
            get = select(user_esp_association.c.esp_id).where(
                user_esp_association.c.user_id == user_id
            )
            result = await self.session.execute(get)
            modules = result.scalars().all()
            return modules
        except exc.SQLAlchemyError as e:
            logger.error(f"Ошибка при получении модулей: {e}")
            raise

    async def get_module(self, key: int) -> Esp:
        """Получение одного модуля по ID. получение полной информации о модуле"""
        try:
            get = select(Esp).where(Esp.id == hash_token(key))
            result = await self.session.execute(get)
            module = result.scalars().first()
            return module
        except exc.SQLAlchemyError as e:
            logger.warning(f"Ошибка при получении данных о модуле {e}")
            raise

    async def update_module(self, key: int, payload: EspUpdate):
        """Обновление модуля по ID."""
        try:
            update_device = (
                update(Esp)
                .where(Esp.hashed_api_key == hash_token(key))
                .values(lat=payload.lat, lon=payload.lon)
            )

            await self.session.execute(update_device)
            await self.session.commit()
            return {"message": "Данные обновлены"}
        except exc.SQLAlchemyError as e:
            logger.critical(f"ошибка при обновлении данных модуля: {e}")
            raise

    async def delete_module(self, esp_id: int, user_id: int):
        """Удаления модуля из списка модулей юзера. Принимает esp_id, user_id"""
        try:
            delete_device = delete(user_esp_association).where(
                user_esp_association.c.esp_id == esp_id,
                user_esp_association.c.user_id == user_id,
            )
            await self.session.execute(delete_device)
            await self.session.commit()
            return {"message": "Модуль удален"}

        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Ошибка при удалении модуля пользователем: {user_id}, модуля {esp_id}. С ошибкой {e}"
            )
            raise

    async def get_irrigation_story(self, esp_id):
        try:
            get = select(SoilMeasurements).where(SoilMeasurements.esp_id == esp_id)
            result = await self.session.execute(get)
            irr_story = result.scalars().first()
            return irr_story
        except exc.SQLAlchemyError as e:
            logger.warning(f"Ошибка при получении данных о модуле {e}")
            raise
