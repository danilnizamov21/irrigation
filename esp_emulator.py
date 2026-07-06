import requests
import random
import time

while True:
    data = {
  "outside_temperature": random.uniform(34.0 , 50.0),
  "inside_temperature": random.uniform(34.0, 50.0),
  "moisture": random.randint(1,21)
}
    
    try:
        r = requests.post("http://127.0.0.1:8000/values/send-values", json=data, timeout=2)
        print(f"Успех: {r.json()}")
    except:
        print(f"Ошибка: {data}")
    
    time.sleep(1)

    