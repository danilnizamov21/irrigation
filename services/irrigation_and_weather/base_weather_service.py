import logging
from abc import ABC, abstractmethod

from services.irrigation_and_weather.weather.fetch_and_analys.data_fetcher import (
    WeatherDataFetcher,
)


class BaseWeatherServiceFetcher(ABC):
    """Абстрактный интерфейс для работы с погодой"""

    @abstractmethod
    async def get_today_weather(self, lat: float, lon: float):
        """получить погодные данные за сегодншний день"""
        pass

    @abstractmethod
    async def get_week_weather(self, lat: float, lon: float):
        pass


class WeatherFetcher(BaseWeatherServiceFetcher):
    """класс наследний реализующий методы для получения погоды на 1 и 7 дней"""

    async def get_today_weather(self, lat, lon):
        """Получение погоды на один день"""
        try:
            fetcher = WeatherDataFetcher(lat, lon, 1)
            days = await fetcher.group_data_by_day()
            if not days:
                logging.warning(
                    f"Метод group_by_day вернул: None."
                    f"Данные lat={lat}, lon={lon}, forecast_days=1"
                )
                raise ValueError("Не удалось получить данные из метода group_by_data")
            day = days[0]
            return day
        except Exception as e:
            logging.critical(
                f"Непредвиденная ошибка при получении погода на текущий день."
                f"Данные lat={lat}, lon={lon}, forecast_days=1"
                f"Ошибка: {e}"
            )
            raise

    async def get_week_weather(self, lat, lon):
        """Получение погоды на недею"""
        try:
            fetcher = WeatherDataFetcher(lat, lon, 7)
            days = await fetcher.group_data_by_day()
            if not days:
                logging.warning(
                    f"Метод group_by_day вернул: None."
                    f"Данные lat={lat}, lon={lon}, forecast_days=7"
                )
                raise ValueError("Не удалось получить данные из метода group_by_data")

            return days
        except Exception as e:
            logging.critical(
                f"Непредвиденная ошибка при получении погода на текущий день."
                f"Данные lat={lat}, lon={lon}, forecast_days=7"
                f"Ошибка: {e}"
            )
            raise
