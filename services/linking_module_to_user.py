from sqlalchemy.ext.asyncio import AsyncSession

from services.check_api_key import get_device_by_key


class Linkin_Module:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def linking_module_to_user(key: str):
        device = await get_device_by_key(key)
        device_id = device.id
        # TODO доделать метод связки модуля с юзером
