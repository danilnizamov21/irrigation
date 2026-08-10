import logging
from datetime import datetime
from typing import Any

import httpx

from core.logger import configure_logging
from schemas.daily_agregate import DailyAgregate

configure_logging()
logger = logging.getLogger(__name__)


class WeatherDataFetcher:
    def __init__(self, lat: float, lon: float, forecast_days: int):
        self.lat = lat
        self.lon = lon
        self.forecast_days = forecast_days
        self._weather_data: dict[str, Any] | None = None

    async def _get_weather_data(self) -> dict[str, Any] | Any | None:
        """Получение данных со стороннего  АПИ"""
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&hourly=temperature_2m,shortwave_radiation,precipitation_probability,precipitation,relative_humidity_2m&timezone=Europe%2FMoscow&forecast_days={self.forecast_days}"

            async with httpx.AsyncClient() as client:
                response = await client.get(url)

            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            logger.critical(
                f"Ошибка при вызове API: {e.response.status_code} URL:{url}"
            )
            raise
        except httpx.RequestError as e:
            logger.critical(f"Сбой или тайм-аут при обращении к API {e.request.url}")
            raise RuntimeError("Не удалось связаться с API") from e
        except Exception as e:
            logger.critical(
                f"Непредвиденная ошибка при попытке связаться с сервером {e}"
            )
            raise

    async def group_data_by_day(self) -> list | None:
        """Группировка данные за один день"""
        try:
            hourly_data = await self.pars_data()
            if hourly_data is None:
                logger.critical("Ошибка при получении спаршенных данных")
                raise ValueError("Не удалось получить данные из pars_data")

            days = {}

            for item in hourly_data:
                date = item["time"][:10]
                if date not in days:
                    dt = datetime.fromisoformat(date)
                    days[date] = DailyAgregate(
                        date=dt,
                        temperatures=[],
                        radiations=[],
                        humidities=[],
                        precipitation=[],
                        precipitation_probabilitys=[],
                    )

                days[date].temperatures.append(item["temperature"])
                days[date].radiations.append(item["radiation"])
                days[date].humidities.append(item["relative_humidity"])
                days[date].precipitation.append(item["precipitation"])
                days[date].precipitation_probabilitys.append(
                    item["precipitation_probability"]
                )

            return list(days.values())
        except Exception as e:
            logger.critical(f"Критическая ошибка при парсинге данных {e}")
            raise

    async def pars_data(self):
        """парсинг данных из JSON в список"""
        try:
            data = await self._get_weather_data()
            if data is None:
                logger.critical(
                    "Ошибка при получении данных из API"
                )  # TODO добавить райз а так же логирование
                raise ValueError("Не удалось получить данные из get_weather_data")
            result = []
            hourly = data.get("hourly", {})
            times = hourly.get("time", [])
            temperature = hourly.get("temperature_2m", [])
            radiation = hourly.get("shortwave_radiation", [])
            precipitation_probability = hourly.get("precipitation_probability", [])
            precipation = hourly.get("precipitation", [])
            relative_humidity = hourly.get("relative_humidity_2m", [])

            for time, temp, rad, prec_prob, prec, rel_hum in zip(
                times,
                temperature,
                radiation,
                precipitation_probability,
                precipation,
                relative_humidity,
            ):
                result.append(
                    {
                        "time": time,
                        "temperature": temp,
                        "radiation": rad,
                        "precipitation_probability": prec_prob,
                        "precipitation": prec,
                        "relative_humidity": rel_hum,
                    }
                )

            return result
        except Exception as e:
            logger.critical(f"Критическая ошибка при парсинге данных {e}")
            raise
