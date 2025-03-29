import json
import logging
from pathlib import Path
from typing import Any, Dict, List, cast

# Создаем директорию для логов относительно корня проекта
project_root = Path(__file__).parent.parent
log_dir = project_root / "logs"
log_dir.mkdir(exist_ok=True)  # Создаем директорию, если ее нет

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Указываем абсолютный путь к файлу логов
log_file = log_dir / "utils.log"
handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_list_dict_transactions(the_way: str) -> List[Dict[str, Any]]:
    try:
        with open(the_way, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.info(f"Успешно загружены данные из файла {the_way}")
            return cast(List[Dict[str, Any]], data)
    except Exception as e:
        logger.error(f"Ошибка при загрузке данных из файла {the_way}: {e}")
        return []


if __name__ == "__main__":
    # Пример использования с абсолютным путем
    transactions_path = project_root / "data" / "transactions.json"  # Пример пути к данным
    transactions = get_list_dict_transactions(str(transactions_path))
    print(transactions)
