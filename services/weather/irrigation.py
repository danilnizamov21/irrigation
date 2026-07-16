import asyncio
import logging

from services.weather.analys import Analys
from services.weather.data_fetcher import WeatherDataFetcher


async def get_irrigation_decision_for_today(
    lat: float, lon: float, forecast_days: int, soil_moisture: int
):
    try:
        c = WeatherDataFetcher(lat, lon, forecast_days)
        analys = Analys()

        days = await c.group_data_by_day()

        if days is None:
            logging.warning(
                f"Метод group_by_day вернул: None."
                f"Данные lat={lat}, lon={lon}, forecast_days={forecast_days}, soil_moisture={soil_moisture}"
            )
            raise ValueError("Не удалось получить данные из метода group_by_data")

        day = days[0]

        calc = Analys.calculate(
            t_max=day.max_temperature,
            t_min=day.min_temperature,
            t_avg=day.avg_temperature,
            rh=day.avg_humidity,
            ghi=day.total_radiation,
        )

        get_status_irrigation = await analys.classifier_data_fetcher(
            calc,
            soil_moisture,
            day.max_precipitation_probability,
            day.total_precipitation,
        )
        irr = analys.analysing_data_classifier(get_status_irrigation)
        print(irr)
    except Exception:
        logging.exception(
            "Критическая ошибка при получении информации о поливе."
            f"Данные lat={lat}, lon={lon}, forecast_days={forecast_days}, soil_moisture={soil_moisture}"
        )
        raise


async def get_weather_forecast_for_seven_days():
    pass


if __name__ == "__main__":
    asyncio.run(get_irrigation_decision_for_today(54.34297, 48.38604, 1, 45))
