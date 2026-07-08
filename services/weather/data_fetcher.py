from typing import Any, Dict, Optional
import httpx


from datetime import datetime
from schemas.daily_agregate import DailyAgregate


class WeatherDataFetcher:
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon
        self._weather_data: Optional[Dict[str, Any]] = None

    async def __get_weather_data(self):
        try:
            if self._weather_data is not None:
                return self._weather_data
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&hourly=temperature_2m,shortwave_radiation,precipitation_probability,precipitation,relative_humidity_2m&timezone=Europe%2FMoscow"
                )

            if response.status_code == 200:
                weather_data = response.json()
                return weather_data
            else:
                print(
                    f"Ошибка при вызове апи: {response.status_code}"
                )  # TODO добавить райз а так же логирование
                return None
        except Exception as e:
            print(f"error {e}")
            return None

    async def group_data_by_day(self):
        hourly_data = await self.pars_data()
        if hourly_data is None:
            print("ошибка при получении распаршенных данных")
            return None

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

    async def pars_data(self):
        data = await self.__get_weather_data()
        if data is None:
            print("возникла ошибка")  # TODO добавить райз а так же логирование
            return
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
