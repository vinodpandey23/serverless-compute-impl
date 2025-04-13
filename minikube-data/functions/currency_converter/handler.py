import json
from utils.converter import get_exchange_rate, convert_currency

def handler(event):
    if isinstance(event, str):
        event = json.loads(event) 
    
    base_currency = event.get("base_currency", "USD")
    target_currency = event.get("target_currency", "EUR")
    amount = event.get("amount", 1)

    rate = get_exchange_rate(base_currency, target_currency)
    if rate is None:
        return {"error": f"Exchange rate not found for {base_currency} to {target_currency}"}
    
    converted_amount = convert_currency(amount, rate)
    return {
        "base_currency": base_currency,
        "target_currency": target_currency,
        "amount": amount,
        "converted_amount": converted_amount
    }
