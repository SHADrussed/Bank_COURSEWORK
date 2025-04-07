from typing import Any

import pytest

from src.processing import sort_by_date

# Общие тестовые данные
common_data = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


@pytest.mark.parametrize(
    "input_data, reverse, expected_output",
    [
        (
            common_data,
            True,
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            common_data,
            False,
            [
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            ],
        ),
        (
            [
                {"id": 123456789, "state": "EXECUTED", "date": "2020-01-01T00:00:00"},
                {"id": 987654321, "state": "CANCELED", "date": "2020-01-01T00:00:00"},
                {"id": 555555555, "state": "PENDING", "date": "2020-01-01T00:00:00"},
            ],
            False,
            [
                {"id": 123456789, "state": "EXECUTED", "date": "2020-01-01T00:00:00"},
                {"id": 987654321, "state": "CANCELED", "date": "2020-01-01T00:00:00"},
                {"id": 555555555, "state": "PENDING", "date": "2020-01-01T00:00:00"},
            ],
        ),
        (
            [
                {"id": 11111111, "state": "EXECUTED", "date": "2020-01-01T00:00:00"},
                {"id": 22222222, "state": "CANCELED", "date": "2020-01-01T00:00:00"},
                {"id": 33333333, "state": "PENDING", "date": "2020-01-01T00:00:00"},
            ],
            False,
            [
                {"id": 11111111, "state": "EXECUTED", "date": "2020-01-01T00:00:00"},
                {"id": 22222222, "state": "CANCELED", "date": "2020-01-01T00:00:00"},
                {"id": 33333333, "state": "PENDING", "date": "2020-01-01T00:00:00"},
            ],
        ),
    ],
)
def test_sort_by_date(input_data: list[dict[str, Any]], reverse: bool, expected_output: list[dict[str, Any]]) -> None:
    """Тестирует функцию sort_by_date с заданными входными данными и ожидаемым результатом.

    Args:
        input_data: Список словарей, который нужно отсортировать.
        reverse: Булевый флаг, указывающий, должна ли сортировка быть в обратном порядке.
        expected_output: Ожидаемый список словарей после сортировки.
    """
    assert sort_by_date(input_data, reverse) == expected_output
