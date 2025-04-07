import pytest

from src.generators import card_number_generator


@pytest.mark.parametrize(
    "floor, ceiling, expected",
    [
        (0, 2, ["0000 0000 0000 0000", "0000 0000 0000 0001", "0000 0000 0000 0002"]),
        (0, 0, ["0000 0000 0000 0000"]),
        (None, None, None),
    ],
)
def test_card_number_generator(floor: int, ceiling: int, expected: list[str]) -> None:
    assert card_number_generator(floor, ceiling) == expected
