


class EvaporationCalculation:
    def __init__(self,
                 evaporation_values: list | None=None,
                 classification_str: list | None=None,
                 ):
        self.evaporation_values = evaporation_values or [2.0, 4.0, 6.0]
        self.classification_str = classification_str or ["low", "middle", "high", "strong"]
        
    @staticmethod
    async def calculate(t_max: float, t_min: float, t_avg: float, rh: int, ghi: float):
        radiation = ghi * 0.0036
        term1 = 0.0118 * (1 - rh / 100) ** 0.2
        term2 = (t_max - t_min) ** 0.3
        term3 = radiation * (t_avg + 10) ** 0.5 - 40
        term4 = 0.1 * (t_avg + 20)
        term5 = 1 - rh / 100
        et = term1 * term2 * term3 + term4 * term5
        return max(0.0, et)

    
    async def classification(self,et: float):
        if et < self.evaporation_values[0]:
            return self.classification_str[0]
        elif self.evaporation_values[0] <= et < self.evaporation_values[1]:
            return self.classification_str[1]
        elif self.evaporation_values[1] <= et <self.evaporation_values[2]:
            return self.evaporation_values[2]
        elif et > self.evaporation_values[2]:
            return self.classification_str[3]
