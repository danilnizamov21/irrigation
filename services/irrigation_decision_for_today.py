import asyncio
import logging

from services.weather.fetch_and_analys.analys import Analys
from services.weather.fetch_and_analys.data_fetcher import WeatherDataFetcher


async def _fetch_current_day_weather(lat: float, lon: float, forecast_days: int):
    try:
        fetcher = WeatherDataFetcher(lat, lon, forecast_days)
        days = fetcher.group_data_by_day()
        if not days:
            logging.warning(
                f"Метод group_by_day вернул: None."
                f"Данные lat={lat}, lon={lon}, forecast_days={forecast_days}"
            )
            raise ValueError("Не удалось получить данные из метода group_by_data")
        day = days[0]
        return day
    except Exception as e:
        logging.critical(
            f"Непредвиденная ошибка при получении погода на текущий день."
            f"Данные lat={lat}, lon={lon}, forecast_days={forecast_days}"
            f"Ошибка: {e}"
        )


async def _determine_irrigation_decision(day, soil_moisture: int):
    """Логика приянтия решения"""
    analys = Analys()
    # Расчет испарения
    calc = analys.calculate(
        t_max=day.max_temperature,
        t_min=day.min_temperature,
        t_avg=day.avg_temperature,
        rh=day.avg_humidity,
        ghi=day.total_radiation,
    )
    # получение классификации для каждого параметра
    get_status_irrigation = await analys.classifier_data_fetcher(  # Передаем данные для классификации их в строку(служит для удобного принятие решений о поливе)
        calc,
        soil_moisture,
        day.max_precipitation_probability,
        day.total_precipitation,
    )
    return analys.analysing_data_classifier(get_status_irrigation)


async def get_irrigation_decision_for_today(
    lat: float, lon: float, forecast_days: int, soil_moisture: int
):
    """Метод для принятия решения о поливе на текущий день"""
    try:
        # получаем данные погода на один день
        current_day_weather = await _fetch_current_day_weather(lat, lon, forecast_days)

        # принятие решения
        decision = _determine_irrigation_decision(current_day_weather, soil_moisture)
        return decision

    except Exception as e:
        logging.exception(
            "Критическая ошибка при получении информации о поливе."
            f"Данные lat={lat}, lon={lon}, forecast_days={forecast_days}, soil_moisture={soil_moisture}"
            f"Ошибка: {e}"
        )
        raise


if __name__ == "__main__":
    asyncio.run(get_irrigation_decision_for_today(54.34297, 48.38604, 1, 45))
