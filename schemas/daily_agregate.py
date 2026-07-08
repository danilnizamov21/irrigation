from datetime import datetime

from typing import List

from pydantic import BaseModel, computed_field


class DailyAgregate(BaseModel):
    date: datetime
    temperatures: List[float]
    radiations: List[int]
    humidities: List[int]
    precipitation: List[float]
    precipitation_probabilitys: List[int]

    @computed_field
    @property
    def max_temperature(self) -> float:
        return max(self.temperatures)

    @computed_field
    @property
    def min_temperature(self) -> float:
        return min(self.temperatures)

    @computed_field
    @property
    def avg_temperature(self) -> float:
        return sum(self.temperatures) / len(self.temperatures)

    @computed_field
    @property
    def total_radiation(self) -> float:
        return sum(self.radiations)

    @computed_field
    @property
    def avg_humidity(self) -> float:
        return sum(self.humidities) / len(self.humidities)

    @computed_field
    @property
    def total_precipitation(self) -> float:
        return sum(self.precipitation)

