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
