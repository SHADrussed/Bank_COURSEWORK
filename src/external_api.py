import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения один раз при запуске приложения
load_dotenv()


def get_amount_of_transaction(transaction: Dict[str, Any]) -> float | None:
    try:
        operation_amount = transaction.get("operationAmount", {})
        amount = float(operation_amount.get("amount"))
        currency = operation_amount.get("currency", {}).get("code")  # Убрано значение по умолчанию USD
    except (AttributeError, TypeError, ValueError, KeyError):
        print("Ошибка в данных")
        return None

    # Если валюта не найдена или не указана
    if not currency:
        return None

    if currency == "RUB":
        return amount

    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
    headers = {"apikey": os.getenv("API_KEY")}
    payload: Dict[str, Any] = {}

    try:
        response = requests.get(url, headers=headers, data=payload)
        response.raise_for_status()
        return float(response.json()["result"])
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None
