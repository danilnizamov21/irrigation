from services.weather.staticmethods import EvaporationCalculation

MIN_MOISTURE_VALUE = 50
class Analys():
    def __init__(self):
        self._calc = EvaporationCalculation()
        
    async def analys_rain(self, precipitation_propability: int,
                          precipitation: float
                          ):
        if precipitation_propability >= 50 and precipitation > 20:
            return {
                "probability": "high",
                "precipitation": "high",
            }
        elif precipitation_propability >= 50 and precipitation < 20:
            return {
                "probability": "high",
                "precipitation": "low",
            }
        elif precipitation_propability < 50 and precipitation > 20:
            return {
                "probability": "low",
                "precipitation": "high",
            }
        else:
            return {
                "probability": "low",
                "precipitation": "low",
            }
        