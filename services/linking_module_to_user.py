import asyncio
import logging

from sqlalchemy import exc, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.esp import Esp
from models.user_esp import user_esp_association
from services.check_api_key import get_device_by_key

logger = logging.getLogger(__name__)


class LinkinModule:
    async def linking_module_to_user(key: str, user_id: int, db: AsyncSession) -> bool:
        try:
            device = await get_device_by_key(key, db)
            linking = insert(user_esp_association).values(
                user_id=user_id, esp_id=device.id
            )
            await db.execute(linking)
            await db.commit()
            return True
        except exc.SQLAlchemyError as e:
            await db.rollback()
            logger.critical(f"Ошибка при попытке связать модуль с юзером: {e}")
            raise

    async def get_user_modules(user_id: int, db: AsyncSession):
        try:
            get = select(user_esp_association.c.esp_id).where(
                user_esp_association.c.user_id == user_id
            )
            result = await db.execute(get)
            modules = result.scalars().all()
            return modules
        except exc.SQLAlchemyError as e:
            logger.error(f"Ошибка при получении модулей: {e}")
            raise

    async def get_module(esp_id: int, db: AsyncSession):
        try:
            get = select(Esp).where(Esp.id == esp_id)
            result = await db.execute(get)
            module = result.scalars().first()
            return module
        except exc.SQLAlchemyError as e:
            logger.warning(f"Ошибка при получении данных о модуле {e}")
            raise


async def main():
    l = LinkinModule
    linking = await l.linking_module_to_user("esp_12eo120w12wl0121ws")
    print(linking)


if __name__ == "__main__":
    asyncio.run(main())
