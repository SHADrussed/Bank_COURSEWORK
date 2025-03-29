from pathlib import Path
from typing import Any, Callable, Union, cast

import pytest

from src.decorators import log


@pytest.fixture
def my_function() -> Callable[[Any, Any], Union[int, None]]:

    @log()
    def my_function(x: Any, y: Any) -> Union[int, None]:
        try:
            return cast(Union[int, None], x + y)
        except TypeError:
            return None

    return my_function


def test_log_ok(capsys: pytest.CaptureFixture[str], my_function: Callable[[Any, Any], Union[int, None]]) -> None:
    my_function(1, 2)
    captured = capsys.readouterr()
    assert captured.out == "my_function ok\n"


@pytest.mark.parametrize(
    "x, y, expected_error",
    [
        (1, "2", "Function returned None due to an error"),
        (1, None, "Function returned None due to an error"),
    ],
)
def test_log_errors(
    capsys: pytest.CaptureFixture[str],
    my_function: Callable[[Any, Any], Union[int, None]],
    x: Any,
    y: Any,
    expected_error: str,
) -> None:
    my_function(x, y)
    captured = capsys.readouterr()
    assert captured.out == f"my_function error {expected_error}. Inputs: ({repr(x)}, {repr(y)}, {{}})\n"


def test_log_file(tmpdir: Path) -> None:
    log_file = tmpdir / "mylog.txt"

    @log(filename=str(log_file))
    def my_function(x: Any, y: Any) -> Union[int, None]:
        try:
            return cast(Union[int, None], x + y)
        except TypeError:
            return None

    my_function(1, None)

    file_content = log_file.read_text(encoding="utf-8")
    expected_content = "my_function error Function returned None due to an error. Inputs: (1, None, " "{})\n"
    assert file_content == expected_content
