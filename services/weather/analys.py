import asyncio
from typing import TypedDict

from classifier import (
    EvaporationClassification,
    MoistureClassification,
    RainClassification,
)
from config import CLASSIFICATION
from staticmethods import EvaporationCalculation


# структура для возвращаемого словаря (analysing)
class AnalysisResult(TypedDict):
    evaporation: str
    moisture: str
    rain: dict[str, str]


class Analys:
    def __init__(self):
        self._calc = EvaporationCalculation()
        self.evp_abs = EvaporationClassification()
        self.rain_abs = RainClassification()
        self.moisture_abs = MoistureClassification()

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
            ): " нужен полив",
            (
                CLASSIFICATION[2],
                CLASSIFICATION[0],
                CLASSIFICATION[0],
                CLASSIFICATION[0],
            ): " нужен полив",
            (
                CLASSIFICATION[3],
                CLASSIFICATION[0],
                CLASSIFICATION[0],
                CLASSIFICATION[0],
            ): " нужен полив",
            (
                CLASSIFICATION[3],
                CLASSIFICATION[2],
                CLASSIFICATION[0],
                CLASSIFICATION[0],
            ): " нужен полив",
            (
                CLASSIFICATION[3],
                CLASSIFICATION[3],
                CLASSIFICATION[0],
                CLASSIFICATION[0],
            ): " нужен полив",
        }
        return RULES.get(current_state, "0")


async def main():
    c = Analys()
    data = AnalysisResult(
        evaporation="low",
        moisture="strong",
        rain={"probability": "low", "precipitation": "low"},
    )
    a = c.analysing_data_classifier(data)
    print(a)


if __name__ == "__main__":
    asyncio.run(main())
