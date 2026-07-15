import asyncio
from typing import  TypedDict

from staticmethods import EvaporationCalculation
from classifier import EvaporationClassification, MoistureClassification, RainClassification
from config import CLASSIFICATION
#структура для возвращаемого словаря (analysing)
class AnalysisResult(TypedDict):
    evaporation: str
    moisture: str
    rain: dict[str, str]

class Analys():
    def __init__(self):
        self._calc = EvaporationCalculation()
        self.evp_abs = EvaporationClassification()
        self.rain_abs = RainClassification()
        self.moisture_abs = MoistureClassification()
        
    
    
    async def classifier_data_fetcher(self,et:float, 
                        soil_moisture:int,
                        precipitation_propability:int, 
                        precipitation:float) -> AnalysisResult:
        
        async with asyncio.TaskGroup() as tg:
            evp_classification = tg.create_task(self.evp_abs.classify(et))
            moisture_classification = tg.create_task(self.moisture_abs.classify(soil_moisture))
            rain_classification = tg.create_task(self.rain_abs.classify(precipitation_propability,precipitation))


        return {"evaporation": evp_classification.result(),
                "moisture": moisture_classification.result(),
                "rain": rain_classification.result()}
    
    async def analysing_data_classifier(data: AnalysisResult):
        if data["evaporation"] == CLASSIFICATION[0]:
            print("low")
        

        
async def main():
    c = Analys()
    
    a = await c.analysing(0.5, 10,50,10.0)
    print(a["evaporation"])

if __name__ == "__main__":
    asyncio.run(main())