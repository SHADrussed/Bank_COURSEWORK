from typing import Any, Generator, Iterable


def filter_by_currency(transactions: Iterable[dict[str, Any]], currency: str) -> list[dict[str, Any]]:
    """Фильтрует транзакции по коду валюты."""
    return [
        transaction
        for transaction in transactions
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency
    ]


def transaction_descriptions(list_of_dict: list[dict[str, Any]], start: int = 0) -> Generator:
    while start <= len(list_of_dict) - 1:
        yield list_of_dict[start].get("description")
        start += 1
    return None


def card_number_generator(start: int, stop: int) -> list[str] | None:
    if start is None or stop is None:
        return None
    list_of_numbers = list(
        map(lambda x: " ".join([x[:4], x[4:8], x[8:12], x[12:]]), [str(i).zfill(16) for i in range(start, stop + 1)])
    )
    return list_of_numbers
