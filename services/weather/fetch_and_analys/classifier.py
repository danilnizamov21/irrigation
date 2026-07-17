from abc import ABC, abstractmethod

from services.weather.fetch_and_analys.config import (
    CLASSIFICATION,
    CLASSIFICATION_ANALYS_RAIN,
    EVAPORATION_VALUES,
    PRECIPATION_PROBABILITY_MIN,
    PROBABILITY_VALUE_MIN,
    SOIL_MOISTURE_HIGH,
    SOIL_MOISTURE_LOW,
    SOIL_MOISTURE_MIDDLE,
)


class BaseClassifier(ABC):
    @abstractmethod
    async def classify(self, **kwargs):
        pass


class EvaporationClassification(BaseClassifier):
    """классификация для исппарения влаги. Возвраащет (low, middle, high, strong)"""

    async def classify(self, et: float, **kwargs) -> str:
        if et < EVAPORATION_VALUES[0]:
            return CLASSIFICATION[0]
        elif EVAPORATION_VALUES[0] <= et < EVAPORATION_VALUES[1]:
            return CLASSIFICATION[1]
        elif EVAPORATION_VALUES[1] <= et < EVAPORATION_VALUES[2]:
            return CLASSIFICATION[2]
        elif et > EVAPORATION_VALUES[2]:
            return CLASSIFICATION[3]


class RainClassification(BaseClassifier):
    """ "классификация для дождя(вероятность осадко и кол-во осадков). Возвращает (low, high)"""

    async def classify(
        self, precipitation_propability: int, precipitation: float
    ) -> dict[str, str]:
        if (
            precipitation_propability >= PRECIPATION_PROBABILITY_MIN
            and precipitation > PROBABILITY_VALUE_MIN
        ):
            return {
                "probability": CLASSIFICATION_ANALYS_RAIN[1],
                "precipitation": CLASSIFICATION_ANALYS_RAIN[1],
            }
        elif (
            precipitation_propability >= PRECIPATION_PROBABILITY_MIN
            and precipitation < PROBABILITY_VALUE_MIN
        ):
            return {
                "probability": CLASSIFICATION_ANALYS_RAIN[1],
                "precipitation": CLASSIFICATION_ANALYS_RAIN[0],
            }
        elif (
            precipitation_propability < PRECIPATION_PROBABILITY_MIN
            and precipitation > PROBABILITY_VALUE_MIN
        ):
            return {
                "probability": CLASSIFICATION_ANALYS_RAIN[0],
                "precipitation": CLASSIFICATION_ANALYS_RAIN[1],
            }
        else:
            return {
                "probability": CLASSIFICATION_ANALYS_RAIN[0],
                "precipitation": CLASSIFICATION_ANALYS_RAIN[0],
            }


class MoistureClassification(BaseClassifier):
    """классификация для влажности внутри земли (принимает один параметр - soil_moisture(floatt))
    возращает - low, middle, high, strong"""

    async def classify(self, soil_moisture: int, **kwargs) -> str:
        if soil_moisture < SOIL_MOISTURE_LOW:
            return CLASSIFICATION[0]
        elif SOIL_MOISTURE_LOW <= soil_moisture < SOIL_MOISTURE_MIDDLE:
            return CLASSIFICATION[1]
        elif SOIL_MOISTURE_MIDDLE <= soil_moisture < SOIL_MOISTURE_HIGH:
            return CLASSIFICATION[2]
        else:
            return CLASSIFICATION[3]
