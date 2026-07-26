from pydantic import BaseModel, Field


class SoilData(BaseModel):
    lat: float
    lon: float
    moisture: int = Field(
        gt=0, le=100, description="Влажность внутри почвы", examples=[50]
    )
