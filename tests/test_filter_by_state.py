from typing import Any

import pytest

from src.processing import filter_by_state


@pytest.mark.parametrize(
    "user_data, state, expected",
    [
        # 1. Стандартные статусы с наличием элементов
        (
            [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}, {"id": 3, "state": "PENDING"}],
            "EXECUTED",
            [{"id": 1, "state": "EXECUTED"}],
        ),
        ([{"id": 4, "state": "EXECUTED"}, {"id": 5, "state": "FAILED"}], "FAILED", [{"id": 5, "state": "FAILED"}]),
        # 2. Нестандартные статусы и типы данных
        ([{"id": 6, "state": 123}, {"id": 7, "state": None}], 123, [{"id": 6, "state": 123}]),
        ([{"id": 8, "state": "executed"}], "EXECUTED", []),
        # 3. Отсутствие элементов с указанным статусом
        ([{"id": 9, "state": "EXECUTED"}, {"id": 10, "state": "CANCELED"}], "PENDING", []),
        # 4. Элементы без ключа 'state'
        ([{"id": 11}, {"id": 12, "state": "EXECUTED"}], "EXECUTED", [{"id": 12, "state": "EXECUTED"}]),
        # 5. Граничные случаи
        ([], "ANY_STATUS", []),  # Пустой список
        (None, "EXECUTED", []),  # None вместо списка
    ],
)
def test_filter_by_state(user_data: list[dict[str, Any]], state: str, expected: list[dict[str, Any]]) -> None:
    assert filter_by_state(user_data, state) == expected
