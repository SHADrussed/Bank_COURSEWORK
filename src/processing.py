from typing import Any, Dict, List  # Импортируем List и Dict для аннотаций


def filter_by_state(list_of_kwargs: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """Фильтрует список по статусу."""
    if not list_of_kwargs:
        return []
    new_list_kwargs: List[Dict[str, Any]] = []
    for i in list_of_kwargs:
        if i.get("state") == state:
            new_list_kwargs.append(i)
    return new_list_kwargs


def sort_by_date(operations: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """Сортирует список словарей по дате."""
    return sorted(operations, key=lambda x: x.get("date", ""), reverse=reverse)
