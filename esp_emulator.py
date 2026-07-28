import random
import time

import requests

while True:
    data = {
        "api_key": "c270027c2c9f1589b865660e4fcb3223c2123c26735d4a8b9f0d9ca55dcfb7bd",
        "moisture": random.randint(1, 100),
    }

    try:
        r = requests.post(
            "http://127.0.0.1:8000/irrigation/telemetry", json=data, timeout=10
        )
        print(f"Успех: {r.json()}")
    except Exception as e:
        print(f"Ошибка: {data}{e}")

    time.sleep(1)
