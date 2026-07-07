from typing import Any, Dict, Optional
import httpx

import asyncio
from datetime import datetime
from schemas.daily_agregate import DailyAgregate
class EvaporationCalculation:
    
    @staticmethod
    async def calculate(
        t_max: float,
        t_min: float,
        rh: int,
        radiation:float
    ):
        t_avg = (t_max + t_min)/2
        term1 = 0.0118 * (rh)**0.2
        term2 = (t_max-t_min)**0.3
        term3 = (radiation*(t_avg+10)**0.5-40)
        term4 = 0.1*(t_avg + 20)
        term5 = (1-rh)
        et = term1*term2*term3+term4*term5
        return et
    
class WeatherAnalysis():
    def __init__(self, lat:float, lon:float,moisture:int):
        self.lat = lat
        self.lon = lon
        self.moisture = moisture
        self._weather_data: Optional[Dict[str, Any]] = None 
    async def __get_weather_data(self):
        try:
            if self._weather_data is not None:
                return self._weather_data
            async with httpx.AsyncClient() as client:
                response = await client.get(f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&hourly=temperature_2m,shortwave_radiation,precipitation_probability,precipitation,relative_humidity_2m&timezone=Europe%2FMoscow")
            
            if response.status_code == 200: 
                weather_data = response.json()
                return weather_data
            else:
                print(f"Ошибка при вызове апи: {response.status_code}") #TODO добавить райз а так же логирование
                return None
        except Exception as e:
            return None
        
    
    async def group_data_by_day(self):
        hourly_data = await self.pars_data()
        if hourly_data is None:
            print("ошибка при получении распаршенных данных")
            return None
        
        days = {}
        
        for item in hourly_data:
            date = item["time"][:10]
            if date not in days:
                dt = datetime.fromisoformat(date)
                days[date] = DailyAgregate(
                    date=dt,
                    temperatures=[],
                    radiations=[],
                    humidities=[],
                    precipitation=[],
                    precipitation_probabilitys=[]
                )
                
            days[date].temperatures.append(item["temperature"])
            days[date].radiations.append(item["radiation"])
            days[date].humidities.append(item["relative_humidity"])
            days[date].precipitation.append(item["precipitation"])
            days[date].precipitation_probabilitys.append(item["precipitation_probability"])
            

        
        return list(days.values())
    async def pars_data(self):
        data=await self.__get_weather_data()
        if data is None:
            print("возникла ошибка") #TODO добавить райз а так же логирование
            return
        result =[]
        hourly = data.get("hourly", {})
        times = hourly.get("time", [])
        temperature  = hourly.get("temperature_2m",[])
        radiation = hourly.get("shortwave_radiation",[])
        precipitation_probability=hourly.get("precipitation_probability",[])
        precipation = hourly.get("precipitation",[])
        relative_humidity = hourly.get("relative_humidity_2m",[])
        for time,temp,rad,prec_prob,prec,rel_hum in zip(times,temperature,radiation,precipitation_probability,precipation,relative_humidity):
            result.append({
                "time": time,
                "temperature": temp,
                "radiation": rad,
                "precipitation_probability": prec_prob,
                "precipitation": prec,
                "relative_humidity": rel_hum
            })
            
          
            
        
       
        return result
        
    
async def main():
    c = WeatherAnalysis(54.34297, 48.38604, 50)
    days = await c.group_data_by_day()
    
    if days:
        # Вывод информации по первому дню
        first_day = days[0]
        print(f"\nПервый день: {first_day.date.date()}")
        print(f"  Температуры: {len(first_day.temperatures)} значений")
        print(f"  Max: {first_day.max_temperature:.1f}°C")
        print(f"  Min: {first_day.min_temperature:.1f}°C")
        print(f"  Avg: {first_day.avg_temperature:.1f}°C")
        print(f"  Осадки: {first_day.total_precipitation:.1f}мм")
        print(f"  Влажность: {first_day.avg_humidity:.1f}%")
        
        # Расчет испаряемости для первого дня
        et = await EvaporationCalculation.calculate(
            t_max=first_day.max_temperature,
            t_min=first_day.min_temperature,
            rh=int(first_day.avg_humidity),
            radiation=first_day.total_radiation
        )
        print(f"  Испаряемость (ET): {et:.2f}")

if __name__ == "__main__":
    asyncio.run(main())
