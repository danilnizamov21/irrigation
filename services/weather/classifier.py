from abc import ABC, abstractmethod
import asyncio

EVAPORATION_VALUES =  [2.0, 4.0, 6.0]
CLASSIFICATION = ["low", "middle", "high", "strong"]

MIN_MOISTURE_VALUE = 50 #%
CLASSIFICATION_ANALYS_RAIN = ['low','high']
PROBABILITY_VALUE_MIN = 20 # mm
PRECIPATION_PROBABILITY_MIN = 50 # % 

SOIL_MOISTURE_LOW = 60    #% 
SOIL_MOISTURE_MIDDLE = 70 #% 
SOIL_MOISTURE_HIGH = 80 #%

class BaseClassifier(ABC):
    @abstractmethod
    async def classify(self, **kwargs):
        pass

class EvaporationClassification(BaseClassifier):
    """классификация для исппарения влаги"""
    async def classify(self,et:float, **kwargs):
        if et < EVAPORATION_VALUES[0]:
            return CLASSIFICATION[0]
        elif EVAPORATION_VALUES[0] <= et < EVAPORATION_VALUES[1]:
            return CLASSIFICATION[1]
        elif EVAPORATION_VALUES[1] <= et < EVAPORATION_VALUES[2]:
            return CLASSIFICATION[2]
        elif et > EVAPORATION_VALUES[2]:
            return CLASSIFICATION[3]
        
class RainClassification(BaseClassifier):
    """"классификация для дождя(вероятность осадко и кол-во осадков)"""
    async def classify(self, precipitation_propability: int,
                          precipitation: float
                          ) -> dict[str,str]:
        if precipitation_propability >= PRECIPATION_PROBABILITY_MIN and precipitation > PROBABILITY_VALUE_MIN:
            return {
                "probability": CLASSIFICATION_ANALYS_RAIN[1],
                "precipitation": CLASSIFICATION_ANALYS_RAIN[1],
            }
        elif precipitation_propability >= PRECIPATION_PROBABILITY_MIN and precipitation < PROBABILITY_VALUE_MIN:
            return {
                "probability": CLASSIFICATION_ANALYS_RAIN[1],
                "precipitation": CLASSIFICATION_ANALYS_RAIN[0],
            }
        elif precipitation_propability < PRECIPATION_PROBABILITY_MIN and precipitation > PROBABILITY_VALUE_MIN:
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
    """классификация для влажности внутри земли"""
    async def classify(self, soil_moisture:int,**kwargs):
        if soil_moisture < SOIL_MOISTURE_LOW:
            return CLASSIFICATION[0]
        elif SOIL_MOISTURE_LOW <= soil_moisture < SOIL_MOISTURE_MIDDLE:
            return CLASSIFICATION[1]
        elif SOIL_MOISTURE_MIDDLE <= soil_moisture < SOIL_MOISTURE_HIGH:
            return CLASSIFICATION[2]
        else:
            return CLASSIFICATION[3]

async def main():
    eveap_cl = MoistureClassification()
    res = await eveap_cl.classify(100)
    print(res)

if __name__ == "__main__":
    asyncio.run(main()) 