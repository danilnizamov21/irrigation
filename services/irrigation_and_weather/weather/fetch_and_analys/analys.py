import asyncio
from typing import TypedDict

from services.irrigation_and_weather.weather.fetch_and_analys.classifier import (
    EvaporationClassification,
    MoistureClassification,
    RainClassification,
)
from services.irrigation_and_weather.weather.fetch_and_analys.config import (
    CLASSIFICATION,
)


# структура для возвращаемого словаря (analysing)
class AnalysisResult(TypedDict):
    evaporation: str
    moisture: str
    rain: dict[str, str]


class Analys:
    def __init__(self):

        self.evp_abs = EvaporationClassification()
        self.rain_abs = RainClassification()
        self.moisture_abs = MoistureClassification()

    @staticmethod
    def calculate(t_max: float, t_min: float, t_avg: float, rh: int, ghi: float):
        """Статический метод для расчета испарения"""
        if (t_max or t_min or t_avg or rh or ghi) < 0.0:
            return 0.0
        radiation = ghi * 0.0036
        term1 = 0.0118 * (1 - rh / 100) ** 0.2
        term2 = (t_max - t_min) ** 0.3
        term3 = radiation * (t_avg + 10) ** 0.5 - 40
        term4 = 0.1 * (t_avg + 20)
        term5 = 1 - rh / 100
        et = term1 * term2 * term3 + term4 * term5
        return max(0.0, et)

    async def classifier_data_fetcher(
        self,
        et: float,
        soil_moisture: int,
        precipitation_propability: int,
        precipitation: float,
    ) -> AnalysisResult:
        """Метод для преобразования данных в виде строк на основе полученных данных из JSON. Взайимодействует с абстрактным классом"""
        async with asyncio.TaskGroup() as tg:
            evp_classification = tg.create_task(self.evp_abs.classify(et))
            moisture_classification = tg.create_task(
                self.moisture_abs.classify(soil_moisture)
            )
            rain_classification = tg.create_task(
                self.rain_abs.classify(precipitation_propability, precipitation)
            )

        return {
            "evaporation": evp_classification.result(),
            "moisture": moisture_classification.result(),
            "rain": rain_classification.result(),
        }

    def analysing_data_classifier(self, data: AnalysisResult):
        """Метод для анализа полученных данных в виде строк(evaporation, moisture,rain_probability,rain_precipitation)"""
        current_state = (
            data["evaporation"],
            data["moisture"],
            data["rain"]["probability"],
            data["rain"]["precipitation"],
        )

        RULES = {
            (
                CLASSIFICATION[0],
                CLASSIFICATION[0],
                CLASSIFICATION[0],
                CLASSIFICATION[0],
            ): "нужен полив",
            (
                CLASSIFICATION[1],
                CLASSIFICATION[0],
                CLASSIFICATION[0],
                CLASSIFICATION[0],
            ): "нужен полив",
            (
                CLASSIFICATION[2],
                CLASSIFICATION[0],
                CLASSIFICATION[0],
                CLASSIFICATION[0],
            ): "нужен полив",
            (
                CLASSIFICATION[3],
                CLASSIFICATION[0],
                CLASSIFICATION[0],
                CLASSIFICATION[0],
            ): "нужен полив",
            (
                CLASSIFICATION[3],
                CLASSIFICATION[2],
                CLASSIFICATION[0],
                CLASSIFICATION[0],
            ): "нужен полив",
            (
                CLASSIFICATION[3],
                CLASSIFICATION[3],
                CLASSIFICATION[0],
                CLASSIFICATION[0],
            ): "нужен полив",
        }
        return RULES.get(current_state, "0")
