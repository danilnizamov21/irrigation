from unittest.mock import AsyncMock

import httpx
import pytest
from payload_json_data import payload_json_for_test_fetch

from services.irrigation_and_weather.weather.fetch_and_analys.data_fetcher import (
    WeatherDataFetcher,
)


class TestWeatherDataFetcher:
    @pytest.fixture
    def fetch(self):
        return WeatherDataFetcher(58, 38, 1)

    @pytest.mark.asyncio
    async def test_get_weather_data(self, respx_mock, fetch):
        respx_mock.get(url__regex=r"https://api\.open-meteo\.com/v1/forecast.*").mock(
            return_value=httpx.Response(200, json=payload_json_for_test_fetch)
        )
        result = await fetch._get_weather_data()
        assert result == payload_json_for_test_fetch

    @pytest.mark.asyncio
    async def test_get_weather_data_statuscode_500(self, respx_mock, fetch):
        respx_mock.get(url__regex=r"https://api\.open-meteo\.com/v1/forecast.*").mock(
            side_effect=httpx.ConnectTimeout("Connection time out")
        )
        with pytest.raises(RuntimeError) as re:
            await fetch._get_weather_data()

        assert "Не удалось связаться с API" in str(re.value)

    @pytest.mark.asyncio
    async def test_get_weather_data_statuscode_exception(self, respx_mock, fetch):
        respx_mock.get(url__regex=r"https://api\.open-meteo\.com/v1/forecast.*").mock(
            side_effect=httpx.InvalidURL("Invalid url")
        )
        with pytest.raises(Exception):
            await fetch._get_weather_data()


class TestParsData:
    @pytest.mark.asyncio
    async def test_pars_data_success(self, mocker):
        fetch = WeatherDataFetcher(58, 38, 1)
        mock_api_response = {
            "hourly": {
                "time": ["2026-07-20T13:00", "2026-07-20T14:00"],
                "temperature_2m": [22.5, 23.0],
                "shortwave_radiation": [450.0, 500.0],
                "precipitation_probability": [10, 23],
                "precipitation": [0.0, 0.1],
                "relative_humidity_2m": [60, 58],
            }
        }

        mocker.patch.object(
            WeatherDataFetcher,
            "_get_weather_data",
            new_callable=AsyncMock,
            return_value=mock_api_response,
        )
        result = await fetch.pars_data()
        assert isinstance(result, list)
        assert len(result) == 2

        assert result[0] == {
            "time": "2026-07-20T13:00",
            "temperature": 22.5,
            "radiation": 450.0,
            "precipitation_probability": 10,
            "precipitation": 0.0,
            "relative_humidity": 60,
        }

    @pytest.mark.asyncio
    async def test_pars_data_error(self):
        pass
