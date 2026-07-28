import pytest

from services.irrigation_and_weather.irrigation_decision_for_today import (
    get_irrigation_decision_for_today,
)


@pytest.mark.parametrize(
    "lat, lon, moisture, expected",
    [(54.43, 48.23, 10, "нужен полив"), (54.43, 48.23, 100, "0")],
)
@pytest.mark.asyncio
async def test_get_irrigation_decision_for_today(lat, lon, moisture, expected):
    get = await get_irrigation_decision_for_today(lat, lon, moisture)
    assert get == expected
