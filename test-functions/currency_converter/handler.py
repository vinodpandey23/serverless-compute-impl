import json
from utils.converter import get_exchange_rate, convert_currency

def handler(context, event):
    # Initialize params as an empty dictionary
    params = {}

    # Check if event.body is not empty and is of bytes type (incoming payload)
    if event.body:
        if isinstance(event.body, bytes):
            try:
                params = json.loads(event.body.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                context.logger.error(f"Failed to decode event body: {str(e)}")
        elif isinstance(event.body, dict):
            # If body is already a dict, use it directly
            params = event.body
        else:
            context.logger.warn(f"Unexpected event.body type: {type(event.body)}")
    
    # Extract parameters from the decoded body, providing default values if needed
    base_currency = params.get("base_currency", "USD")
    target_currency = params.get("target_currency", "EUR")
    amount = params.get("amount", 1)

    # Convert amount to float (or int) to ensure correct math operations
    try:
        amount = float(amount)  # Ensure amount is a number
    except ValueError:
        context.logger.error(f"Invalid 'amount' value: {amount}. Must be a number.")
        return {"error": f"Invalid 'amount' value: {amount}. Must be a number."}

    # Fetch the exchange rate
    rate = get_exchange_rate(base_currency, target_currency)
    if rate is None:
        return {"error": f"Exchange rate not found for {base_currency} to {target_currency}"}
    
    # Convert the amount based on the fetched rate
    converted_amount = convert_currency(amount, rate)
    
    # Return the response with the conversion result
    return {
        "base_currency": base_currency,
        "target_currency": target_currency,
        "amount": amount,
        "converted_amount": converted_amount
    }
