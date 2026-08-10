import asyncio
import logging

from services.irrigation_and_weather.base_weather_service import WeatherFetcher
from services.irrigation_and_weather.irrigation_decision_for_today import (
    _determine_irrigation_decision,
)

logger = logging.getLogger(__name__)


async def agregate_data(days):
    """Парс данных погоды на 7 дней в виде ключ-значение"""
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


async def agregate_by_day(agregate):
    async with asyncio.TaskGroup() as tg:
        day1 = tg.create_task(_determine_irrigation_decision(agregate[0], 60))
        day2 = tg.create_task(_determine_irrigation_decision(agregate[1], 60))
        day3 = tg.create_task(_determine_irrigation_decision(agregate[2], 60))
        day4 = tg.create_task(_determine_irrigation_decision(agregate[3], 60))
        day5 = tg.create_task(_determine_irrigation_decision(agregate[4], 60))
        day6 = tg.create_task(_determine_irrigation_decision(agregate[5], 60))
        day7 = tg.create_task(_determine_irrigation_decision(agregate[6], 60))
        # TODO ДОДЕЛАТЬ ПЕРЕДАЧУ И АНАЛИЗ ДАННЫХ НА КАЖДЫЙ ДЕНЬ

    return {
        "1": day1.result(),
        "2": day2.result(),
        "3": day3.result(),
        "4": day4.result(),
        "5": day5.result(),
        "6": day6.result(),
        "7": day7.result(),
    }


async def get_weather_forecast_for_week(lat: float, lon: float):
    fetcher_week = WeatherFetcher()
    week_forecast = await fetcher_week.get_week_weather(lat, lon)
    if week_forecast is None:
        logger.critical(
            "Пустой список данных при вызове get_week_weather"
            f"Данные lat={lat} lon={lon}"
        )
        raise ValueError("Ошибка при получении данных")
    return week_forecast


async def main():
    a = await get_weather_forecast_for_week(54.34297, 48.38604)
    b = await agregate_by_day(a)
    print(b)


if __name__ == "__main__":
    asyncio.run(main())
