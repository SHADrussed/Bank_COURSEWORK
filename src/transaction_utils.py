import re

def filter_transactions_by_description(transactions: list[dict], search_pattern: str) -> list[dict]:
    """
    Фильтрует список транзакций, оставляя только те, в описании которых встречается заданная строка (с учётом регистра).

    Args:
        transactions: Список словарей с данными о транзакциях.
        search_pattern: Строка для поиска в поле 'description'.

    Returns:
        Список отфильтрованных транзакций, где description содержит search_pattern.
    """
    filtered_transactions = []
    for transaction in transactions:
        description = transaction.get("description", "")
        if re.search(search_pattern, description):
            filtered_transactions.append(transaction)
    return filtered_transactions


def count_transactions_by_categories(transactions: list[dict], categories: list[str]) -> dict[str, int]:
    """
    Подсчитывает количество транзакций по категориям, проверяя наличие категории в поле `description`.

    Args:
        transactions: Список транзакций (словарей с данными).
        categories: Список категорий для поиска (регистронезависимо).

    Returns:
        Словарь {категория: количество_совпадений}.
    """
    # Удаление дубликатов с сохранением порядка
    seen = set()
    unique_categories = [cat for cat in categories if not (cat in seen or seen.add(cat))]

    counts = {category: 0 for category in unique_categories}

    for transaction in transactions:
        description = transaction.get("description", "")
        for category in unique_categories:
            pattern = re.escape(category)
            if re.search(pattern, description, flags=re.IGNORECASE):
                counts[category] += 1
    return counts


