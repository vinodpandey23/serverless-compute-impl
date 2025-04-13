import requests

def get_exchange_rate(base_currency, target_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    response.raise_for_status()
    rates = response.json().get("rates", {})
    return rates.get(target_currency, None)

def convert_currency(amount, rate):
    return round(amount * rate, 2)
