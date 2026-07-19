import pytest

from services.irrigation_and_weather.weather.fetch_and_analys.classifier import (
    EvaporationClassification,
    RainClassification,
)
from services.irrigation_and_weather.weather.fetch_and_analys.config import (
    CLASSIFICATION,
    CLASSIFICATION_ANALYS_RAIN,
)


@pytest.mark.parametrize(
    "et, expected",
    [(1.0, CLASSIFICATION[0]), (2.0, CLASSIFICATION[1]), (5.0, CLASSIFICATION[2])],
)
@pytest.mark.asyncio
async def test_evaporation_classification(et, expected):
    evp_cls = EvaporationClassification()
    result = await evp_cls.classify(et)
    assert result == expected


@pytest.mark.parametrize(
    "precipitation_probability, precipitation,expected_probability, expected_precipitation",
    [(10, 2.0, CLASSIFICATION_ANALYS_RAIN[0], CLASSIFICATION_ANALYS_RAIN[0])],
)
@pytest.mark.asyncio
async def test_rain_classification(
    precipitation_probability,
    precipitation,
    expected_probability,
    expected_precipitation,
):
    rain_cls = RainClassification()
    result = await rain_cls.classify(precipitation_probability, precipitation)
    assert result["probability"] == expected_probability, (
        result["precipitation"] == expected_precipitation
    )


@pytest.mark.asyncio
async def test_moisture_classification():
    pass
