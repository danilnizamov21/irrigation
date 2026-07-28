from unittest.mock import AsyncMock

import pytest

from services.irrigation_and_weather.weather.fetch_and_analys.analys import (
    Analys,
    AnalysisResult,
)
from services.irrigation_and_weather.weather.fetch_and_analys.config import (
    CLASSIFICATION,
    CLASSIFICATION_ANALYS_RAIN,
)


@pytest.mark.parametrize(
    "t_max, t_min, t_avg, rh, ghi",
    [
        (30, 15, 20, 50, 300),
        (34.4, 10.2, 22, 40, 400),
        (-21, -10, -16.55, -30, -10),
        (40.23, 10.1, 25, 15, 600),
    ],
)
def test_calculate_evaporation_positive(t_max, t_min, t_avg, rh, ghi):
    """Тестирование метода расчета испарения с отрицательными и положительными значениями"""
    evaporation_calculate = Analys.calculate(t_max, t_min, t_avg, rh, ghi)
    assert evaporation_calculate >= 0.0


@pytest.mark.asyncio
async def test_classifier_data_fetcher():
    """Тестирование метода получения статусов в виде строковых значений"""
    analys = Analys()

    analys.evp_abs.classify = AsyncMock(return_value=CLASSIFICATION[3])
    analys.moisture_abs.classify = AsyncMock(return_value=CLASSIFICATION[1])

    fake_rain_analys = {
        "probability": CLASSIFICATION_ANALYS_RAIN[0],
        "precipitation": CLASSIFICATION_ANALYS_RAIN[0],
    }
    analys.rain_abs.classify = AsyncMock(return_value=fake_rain_analys)

    result = await analys.classifier_data_fetcher(
        et=2.3, soil_moisture=40, precipitation_propability=30, precipitation=0.3
    )
    assert result["evaporation"] == CLASSIFICATION[3]
    assert result["moisture"] == CLASSIFICATION[1]
    assert result["rain"] == fake_rain_analys

    analys.evp_abs.classify.assert_called_once_with(2.3)
    analys.moisture_abs.classify.assert_called_once_with(40)
    analys.rain_abs.classify.assert_called_once_with(30, 0.3)


@pytest.mark.parametrize(
    "evp, moist, probability, precipitation, expected",
    [
        (
            CLASSIFICATION[0],
            CLASSIFICATION[0],
            CLASSIFICATION[0],
            CLASSIFICATION[0],
            "нужен полив",
        ),
        (
            CLASSIFICATION[1],
            CLASSIFICATION[0],
            CLASSIFICATION[0],
            CLASSIFICATION[0],
            "нужен полив",
        ),
        (
            CLASSIFICATION[2],
            CLASSIFICATION[0],
            CLASSIFICATION[0],
            CLASSIFICATION[0],
            "нужен полив",
        ),
        (
            CLASSIFICATION[3],
            CLASSIFICATION[3],
            CLASSIFICATION[3],
            CLASSIFICATION[3],
            "0",
        ),
        (
            CLASSIFICATION[2],
            CLASSIFICATION[2],
            CLASSIFICATION[2],
            CLASSIFICATION[2],
            "0",
        ),
    ],
)
def test_analysing_data_classifier(evp, moist, probability, precipitation, expected):
    """Тестирование обработки классификаций значений погоды.
    В данной функции тестируются значения которые должны вернуть положительный результат то есть - "нужен полив" а так же отрицательный - "0" """
    analys = Analys()
    data: AnalysisResult = {
        "evaporation": evp,
        "moisture": moist,
        "rain": {
            "probability": probability,
            "precipitation": precipitation,
        },
    }
    result = analys.analysing_data_classifier(data)
    assert result == expected
