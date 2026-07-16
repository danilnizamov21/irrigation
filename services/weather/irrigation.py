import asyncio

from services.weather.analys import Analys
from services.weather.data_fetcher import WeatherDataFetcher


async def main():
    c = WeatherDataFetcher(54.34297, 48.38604)
    days = await c.group_data_by_day()
    if days is not None:
        for i in range(len(days)):
            day = days[i]

            calc = Analys.calculate(
                t_max=day.max_temperature,
                t_min=day.min_temperature,
                t_avg=day.avg_temperature,
                rh=day.avg_humidity,
                ghi=day.total_radiation,
            )
            a = Analys()
            analys = await a.classifier_data_fetcher(
                calc, 10, day.max_precipitation_probability, day.total_precipitation
            )
            irr = a.analysing_data_classifier(analys)
            print(irr)


if __name__ == "__main__":
    asyncio.run(main())
