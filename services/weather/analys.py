from services.weather.staticmethods import EvaporationCalculation

MIN_MOISTURE_VALUE = 50
CLASSIFICATION_ANALYS_RAIN = ['low','high']
PROBABILITY_VALUE_MIN = 20 # mm
PRECIPATION_PROBABILITY_MIN = 50 # % 
class Analys():
    def __init__(self):
        self._calc = EvaporationCalculation()
        
    
    
    async def analysing(self,probability: str, precipitation: str, classification_evaporation: str):
        pass
        