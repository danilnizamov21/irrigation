from schemas.irigation import SoilData
class IrigationClass:
    def __init__(self, data: SoilData):
        self.data = data
        

    async def check_temp(self):
        if self.data.outside_temperature > 30 and self.data.inside_temperature > 30 and self.data.moisture < 30:
            return {"pump": 1}
        else:
            return{"pump": 0}
        
    