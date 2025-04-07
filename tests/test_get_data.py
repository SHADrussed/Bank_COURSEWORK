import pytest

from src.widget import get_data


@pytest.mark.parametrize(
    "user_data, expected",
    [
        # Стандартный формат ISO 8601
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        # Дата без времени
        ("2024-03-11", "11.03.2024"),
        # Граничные случаи
        ("0001-01-01T00:00:00", "01.01.0001"),  # Минимальная дата
        ("9999-12-31T23:59:59.999999", "31.12.9999"),  # Максимальная дата
        # Нестандартные форматы (должны возвращать None)
        ("11/03/2024", None),  # Неправильный формат
        ("March 11, 2024", None),  # Текстовый формат
        # Отсутствие даты
        (None, None),  # Нет даты
        ("", None),  # Пустая строка
    ],
)
def test_get_data(user_data: str, expected: str | None) -> None:
    assert get_data(user_data) == expected
