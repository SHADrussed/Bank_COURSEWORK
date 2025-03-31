import math
from datetime import datetime
from dateutil.parser import parse
from src.transaction_reader import (
    read_transactions_from_csv,
    read_transactions_from_excel,
)
from src.utils import get_list_dict_transactions
from src.transaction_utils import filter_transactions_by_description
from src.masks import get_mask_card_number, get_mask_account


def mask_account(account: str) -> str:
    """Маскирует номер карты/счета"""
    if not account or (isinstance(account, float) and math.isnan(account)):
        return ""

    account_str = str(account)

    try:
        if "Счет" in account_str:
            numbers = "".join(filter(str.isdigit, account_str))
            return f"Счет {get_mask_account(int(numbers))}" if numbers else account_str
        else:
            parts = account_str.split()
            numbers = "".join(filter(str.isdigit, account_str))
            card_name = " ".join([p for p in parts if not p.isdigit()])
            return f"{card_name} {get_mask_card_number(int(numbers))}" if numbers else account_str

    except Exception as e:
        print(f"Ошибка маскировки: {e}")
        return account_str


def print_transaction(transaction):
    """Улучшенный вывод транзакций"""
    try:
        # Форматирование даты
        raw_date = transaction.get('date', '')
        date_obj = parse(raw_date) if raw_date else None
        date = date_obj.strftime("%d.%m.%Y") if date_obj else raw_date

        # Маскировка счетов
        from_acc = mask_account(transaction.get('from', ''))
        to_acc = mask_account(transaction.get('to', ''))

        # Форматирование валюты
        currency_code = transaction.get('currency_code', '')
        currency = "руб." if currency_code == "RUB" else currency_code

        print(
            f"{date} {transaction.get('description', '')}\n"
            f"{from_acc} -> {to_acc}\n"
            f"Сумма: {transaction.get('amount', '')} {currency}\n"
        )

    except Exception as e:
        print(f"Ошибка вывода транзакции: {e}")


def main():
    # Инициализация
    print("Привет! Добро пожаловать в программу работы с транзакциями")

    # Выбор файла
    file_choice = input("""Программа: Привет! Добро пожаловать в программу работы 
с банковскими транзакциями. 
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла\n\n"""
    )

    # Загрузка данных
    try:
        if file_choice == '1':
            transactions = get_list_dict_transactions(r"D:\PythonProjects\Bank_Homework\data\operations.json")
        elif file_choice == '2':
            transactions = read_transactions_from_csv(r"D:\PythonProjects\Bank_Homework\data\transactions.csv")
        elif file_choice == '3':
            transactions = read_transactions_from_excel(r"D:\PythonProjects\Bank_Homework\data\transactions_excel.xlsx")
        else:
            print("Неверный выбор!")
            return
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return

    # Фильтрация по статусу
    while True:
        status = input("Введите статус (EXECUTED/CANCELED/PENDING): ").upper()
        if status in {'EXECUTED', 'CANCELED', 'PENDING'}:
            break
        print("Некорректный статус!")

    filtered = [
        t for t in transactions
        if str(t.get('state', '')).upper() == status
    ]

    # Сортировка
    if input("Сортировать по дате? (да/нет): ").lower() == 'да':
        filtered.sort(
            key=lambda x: parse(x['date']) if x.get('date') else datetime.min,
            reverse=input("Порядок (возрастание/убывание): ").lower() == 'убывание'
        )

    # Дополнительные фильтры
    if input("Только рубли? (да/нет): ").lower() == 'да':
        filtered = [t for t in filtered if t.get('currency_code') == 'RUB']

    if input("Фильтр по описанию? (да/нет): ").lower() == 'да':
        search = input("Введите поисковый запрос: ")
        filtered = filter_transactions_by_description(filtered, search)

    # Вывод результатов
    if not filtered:
        print("Нет транзакций по заданным критериям")
        return

    print(f"\nНайдено транзакций: {len(filtered)}\n")
    for i, t in enumerate(filtered, 1):
        print(f"Транзакция #{i}")
        print_transaction(t)
        print("-" * 50)


if __name__ == "__main__":
    main()