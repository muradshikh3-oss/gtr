import requests
from config import API_KEY

def get_weather(city: str) -> str:
    """Показыавет погоду"""
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200:
        return f"Не удалось найти город: {city}"

    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]

    return f"{city}: {temp}°C, {description}"

def get_rate(base: str, target: str) -> str:
    """Показывает курс валюты"""
    base = base.upper()
    target = target.upper()

    url = f"https://open.er-api.com/v6/latest/{base}"

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return "Не удалось получить курс"

    if data.get("result") != "success":
        return "Не удалось получить курс"

    rates = data["rates"]

    if target not in rates:
        return f"Валюта {target} не найдена"

    rate = rates[target]

    return f"1 {base} = {rate} {target}"
