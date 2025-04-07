from typing import Any
from unittest.mock import patch

from src.external_api import get_amount_of_transaction


@patch("requests.get")
def test_get_amount_of_transaction_normal(mock_get: Any) -> None:
    mock_get.return_value.json.return_value = {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": 31957.58},
        "info": {"timestamp": 1742184303, "rate": 85.424159},
        "date": "2025-03-17",
        "result": 2729949.395175,
    }
    assert (
        get_amount_of_transaction(
            {
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "operationAmount": {"amount": "31957.58", "currency": {"name": "USD", "code": "USD"}},
            }
        )
        == 2729949.395175
    )


def test_get_amount_of_transaction_error() -> None:
    transaction = {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {"amount": "31957.58"},
    }

    result = get_amount_of_transaction(transaction)
    assert result is None


def test_get_amount_of_transaction_another() -> None:
    transaction: dict[str, Any] = {}

    result = get_amount_of_transaction(transaction)
    assert result is None


@patch("requests.get")
def test_get_amount_of_transaction_rub(mock_get: Any) -> None:
    transaction = {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {"amount": "1000.00", "currency": {"name": "RUB", "code": "RUB"}},
    }

    result = get_amount_of_transaction(transaction)
    assert result == 1000.00
