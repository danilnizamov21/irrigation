from pydantic import BaseModel, Field


class SoilData(BaseModel):
    hashed_api_key: str = Field(description="уникальный ключ каждого устроуства")
    moisture: int = Field(
        gt=0, le=100, description="Влажность внутри почвы", examples=[50]
    )
