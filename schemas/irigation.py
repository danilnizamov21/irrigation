from pydantic import BaseModel, Field

class SoilData(BaseModel):
    outside_temperature: float = Field(gt=0.0, le=50.0,description="Температура на улице в цельсиях", examples=[22.5])
    inside_temperature: float = Field(gt=0.0, le=50.0, description="Температура внутри почвы", examples=[22.5])
    moisture: int = Field(gt=0, le=100,description="Влажность внутри почвы", examples=[50])

    