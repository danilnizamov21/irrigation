# from fastapi import Depends, FastAPI
# from pydantic import BaseModel
# from api.irigation import router as send_values
# app = FastAPI()

# app.include_router(send_values, prefix="/values", tags=["Values"])
import asyncio

from services.weather.staticmethods import EvaporationCalculation
from services.weather.data_fetcher import WeatherDataFetcher


async def main():
    c = WeatherDataFetcher(54.34297, 48.38604)
    days = await c.group_data_by_day()
    if days is not None:
        for i in range(len(days)):
            day = days[i]
       
            calc = await EvaporationCalculation.calculate(t_max=day.max_temperature,
                                                       t_min=day.min_temperature,
                                                       t_avg=day.avg_temperature,
                                                       rh=day.avg_humidity,
                                                       ghi=day.total_radiation)
            print(calc)
if __name__ == "__main__":
    asyncio.run(main())
