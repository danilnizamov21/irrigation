from unittest.mock import AsyncMock, MagicMock

import pytest

from services.auth.auth import AuthService


@pytest.mark.asyncio
async def test_get_user_by_login_returns_user():
    session = MagicMock()
    redis = MagicMock()

    user = MagicMock()

    result = MagicMock()
    result.scalar_one_or_none.return_value = user

    session.execute = AsyncMock(return_value=result)

    service = AuthService(session, redis)

    result_user = await service.get_user_by_login("danil")

    assert result_user is user
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_user_by_login_raises_database_error():
    session = MagicMock()
    redis = MagicMock()

    session.execute = AsyncMock(side_effect=Exception("Database connection error"))

    service = AuthService(session, redis)

    with pytest.raises(Exception, match="Database connection error"):
        await service.get_user_by_login("danil")
