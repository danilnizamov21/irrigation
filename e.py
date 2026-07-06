import requests

class WeatherAnalysis():
    def __init__(self, lat:float, lon:float):
        self.lat = lat
        self.lon = lon

    def __get_weather_data(self):
        try:
            response =  requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&hourly=temperature_2m,cloud_cover,precipitation,precipitation_probability&timezone=Europe%2FMoscow")
            if response.status_code == 200: 
                self.weather_data = response.json()
                return self.weather_data
            else:
                print(f"Ошибка при вызове апи: {response.status_code}")
                return None
        except Exception as e:
            return None
        
    def analys_data(self):
        self.__get_weather_data()
        hourly = self.weather_data.get("hourly", {})
        times = hourly.get("time", [0])
        for t in times:
            print(f"  {t}")

if __name__ == "__main__":
    c = WeatherAnalysis(54.32, 48.38)
    c.analys_data()
