from functools import wraps
from typing import Any, Callable, Optional, TypeVar, cast

# Define a type variable for the return type of the decorated function
F = TypeVar("F", bound=Callable[..., Any])


def log(filename: Optional[str] = None) -> Callable[[F], F]:
    """
    Декоратор для логирования вызовов функций и их результатов или ошибок.

    Args:
        filename (Optional[str]): Имя файла для логирования. Если None, выводит в stdout.

    Returns:
        Callable[[F], F]: Декорированная функция.
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                # Если функция вернула None, считаем это ошибкой
                if result is None:
                    raise TypeError("Function returned None due to an error")
                message = f"{func.__name__} ok\n"
            except Exception as e:
                message = f"{func.__name__} error {e}. Inputs: ({', '.join(map(repr, args))}, {kwargs})\n"
                result = None  # Возвращаем None в случае ошибки

            if filename is None:
                print(message, end="")
            else:
                with open(filename, "a", encoding="utf-8") as file:
                    file.write(message)

            return result

        return cast(F, wrapper)  # Явное приведение типа

    return decorator
