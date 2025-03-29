from unittest.mock import Mock, mock_open, patch

from src.transaction_reader import read_transactions_from_csv, read_transactions_from_excel


def test_read_transactions_from_csv():
    """Тестирует чтение данных из CSV файла с использованием моков."""
    expected_data = [
        {"id": "1", "amount": "100", "category": "food"},
        {"id": "2", "amount": "200", "category": "transport"},
    ]

    # Мокаем встроенную функцию open и csv.DictReader
    mock_file = mock_open()
    with patch("builtins.open", mock_file), patch("csv.DictReader") as mock_reader:
        mock_reader.return_value = expected_data
        result = read_transactions_from_csv("test.csv")

        # Проверяем вызовы и результат
        mock_file.assert_called_once_with("test.csv", "r", encoding="utf-8")
        mock_reader.assert_called_once_with(mock_file.return_value)
        assert result == expected_data


def test_read_empty_csv():
    """Тестирует обработку пустого CSV файла."""
    mock_file = mock_open()
    with patch("builtins.open", mock_file), patch("csv.DictReader") as mock_reader:
        mock_reader.return_value = []
        result = read_transactions_from_csv("empty.csv")
        assert result == []


def test_read_transactions_from_excel():
    """Тестирует чтение данных из Excel файла с использованием моков."""
    expected_data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]

    # Создаем мок DataFrame и настраиваем его поведение
    mock_df = Mock()
    mock_df.to_dict.return_value = expected_data

    # Мокаем pandas.read_excel
    with patch("pandas.read_excel", return_value=mock_df) as mock_read:
        result = read_transactions_from_excel("test.xlsx")

        # Проверяем вызовы и результат
        mock_read.assert_called_once_with("test.xlsx")
        mock_df.to_dict.assert_called_once_with("records")
        assert result == expected_data


def test_read_empty_excel():
    """Тестирует обработку пустого Excel файла."""
    mock_df = Mock()
    mock_df.to_dict.return_value = []

    with patch("pandas.read_excel", return_value=mock_df):
        result = read_transactions_from_excel("empty.xlsx")
        assert result == []
