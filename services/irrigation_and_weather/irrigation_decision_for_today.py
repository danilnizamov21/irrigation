import logging

from services.irrigation_and_weather.base_weather_service import WeatherFetcher
from services.irrigation_and_weather.weather.fetch_and_analys.analys import Analys

logger = logging.getLogger(__name__)


async def _determine_irrigation_decision(day, soil_moisture: int) -> str:
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
    status = analys.analysing_data_classifier(get_status_irrigation)

    return status


async def get_irrigation_decision_for_today(lat: float, lon: float, soil_moisture: int):
    """Метод для принятия решения о поливе на текущий день"""
    try:
        day_weather = WeatherFetcher()
        # получаем данные погода на один день
        current_day_weather = await day_weather.get_today_weather(lat, lon)

        # принятие решения
        decision = await _determine_irrigation_decision(
            current_day_weather, soil_moisture
        )
        print(decision)
        return decision

    except Exception as e:
        logger.exception(
            "Критическая ошибка при получении информации о поливе."
            f"Данные lat={lat}, lon={lon}, soil_moisture={soil_moisture}"
            f"Ошибка: {e}"
        )
        raise


# if __name__ == "__main__":
#     asyncio.run(get_irrigation_decision_for_today(54.34297, 48.38604, 10))
