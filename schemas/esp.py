from pydantic import BaseModel, Field


class SoilData(BaseModel):
    api_key: str = Field(description="уникальный ключ каждого устроуства")
    moisture: int = Field(
        gt=0, le=100, description="Влажность внутри почвы", examples=[50]
    )


class EspResponse(BaseModel):
    lat: float
    lon: float


class EspUpdate(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)


class EspCreateResponse(BaseModel):
    id: int
    api: str
