import pytest

from src.masks import get_mask_account


@pytest.mark.parametrize(
    "card_number, expected",
    [
        (73654108430135874305, "**4305"),  # Длинный номер счета
        (1234567890123456, "**3456"),  # Средний номер счета
        (1234, "**34"),  # Номер счета из 4 цифр
        (123, "**3"),  # Номер счета из 3 цифр (короткий)
        (0, "*"),  # Номер счета из 1 цифры (короткий)
        (None, ""),
    ],
)
def test_get_mask_account(card_number: int, expected: str) -> None:
    assert get_mask_account(card_number) == expected
