import asyncio
import logging

from services.irrigation_and_weather.base_weather_service import WeatherFetcher


async def agregate_data(days):

    agregate = {}
    for day in days:
        date = day.date
        agregate[date] = {
            "max_temperature": day.max_temperature,
            "min_temperature": day.min_temperature,
            "avg_temperature": day.avg_temperature,
            "total_radiation": day.total_radiation,
            "avg_humidity": day.avg_humidity,
            "total_precipitation": day.total_precipitation,
            "max_precipitation_probability": day.max_precipitation_probability,
        }
    return agregate


async def get_weather_forecast_for_week(lat: float, lon: float):
    fetcher_week = WeatherFetcher()
    week_forecast = await fetcher_week.get_week_weather(lat, lon)
    if week_forecast is None:
        logging.critical(
            "Пустой список данных при вызове get_week_weather"
            f"Данные lat={lat} lon={lon}"
        )
        raise ValueError("Ошибка при получении данных")
    await agregate_data(week_forecast)
    return


async def main():
    a = await get_weather_forecast_for_week(54.34297, 48.38604)
    return a


if __name__ == "__main__":
    asyncio.run(main())
