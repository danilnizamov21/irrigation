from datetime import datetime
import random
from typing import List

from pydantic import BaseModel, computed_field
# "temp": [],
# "radiations": [],
# "humidities": [],
# "precipitation": [],
# "precipitation_probabilities": []
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
    def min_temperature(self)-> float:
        return min(self.temperatures)
    @computed_field
    @property
    def avg_temperature(self) -> float:
        return sum(self.temperatures) / len(self.temperatures)
    @computed_field
    @property
    def total_radiation(self)-> float:
        return sum(self.radiations)
    @computed_field
    @property
    def avg_humidity(self)-> float:
        return sum(self.humidities) / len(self.humidities)
    @computed_field
    @property
    def total_precipitation(self) -> float:
        return sum(self.precipitation)
    

def test():
    temps = []
    rads = []
    hums = []
    precs = []
    prec_probs = []
    
    for _ in range(24):
        temps.append(random.uniform(15.0, 35.0))
        rads.append(random.randint(0, 800))
        hums.append(random.randint(30, 90))
        precs.append(random.uniform(0.0, 10.0))
        prec_probs.append(random.randint(0, 100))
    
    
    daily = DailyAgregate(
        date = datetime.now(),
        temperatures=temps,
        radiations=rads,
        humidities=hums,
        precipitation=precs,
        precipitation_probabilitys=prec_probs
    )
    
    
    print(f"Макс температура: {daily.max_temperature:.1f}°C")
    print(f"Средняя влажность: {daily.avg_humidity:.1f}%")
    print(f"Общее кол-во осадков: {daily.total_precipitation:.1f}mm")
    
    return daily


if __name__ == "__main__":
    test()