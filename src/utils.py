import json
import logging
import math
from pathlib import Path
from typing import Any, Dict, List, cast

project_root = Path(__file__).parent.parent
log_dir = project_root / "logs"
log_dir.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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

            # Очищаем данные от NaN
            cleaned_data = []
            for item in data:
                cleaned_item = {
                    k: v if not (isinstance(v, float) and math.isnan(v)) else None
                    for k, v in item.items()
                }
                cleaned_data.append(cleaned_item)

            logger.info(f"Успешно загружены данные из файла {the_way}")
            return cast(List[Dict[str, Any]], cleaned_data)

    except Exception as e:
        logger.error(f"Ошибка при загрузке данных из файла {the_way}: {e}")
        return []

