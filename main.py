# from fastapi import Depends, FastAPI
# from pydantic import BaseModel
# from api.irigation import router as send_values
# app = FastAPI()

# app.include_router(send_values, prefix="/values", tags=["Values"])
import asyncio

from services.weather_analys.analys_weather import EvaporationCalculation, WeatherAnalysis


async def main():
    c = WeatherAnalysis(54.34297, 48.38604, 50)
    days = await c.group_data_by_day()
    if days is not None:
        for i in range(7):
            day = days[i]
            date = day.date
            print(date)

if __name__ == "__main__":
    asyncio.run(main())
