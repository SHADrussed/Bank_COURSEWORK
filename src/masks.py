import logging

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.DEBUG

logger = logging.getLogger("masks")
logger.setLevel(LOG_LEVEL)

file_handler = logging.FileHandler(
    r"D:\PythonProjects\Bank_Homework\logs\masks.log", mode="a", encoding="utf-8", delay=False
)
file_handler.setLevel(LOG_LEVEL)

formatter = logging.Formatter(LOG_FORMAT)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


logging.getLogger().setLevel(logging.DEBUG)


def get_mask_card_number(card_number: int) -> str:
    """Функция маскировки номера банковской карты"""
    if card_number is None:
        logger.warning("Передано пустое значение номера карты.")
        return ""

    refactored_card_number: str = str(card_number)
    scale_of_number = len(refactored_card_number)

    if scale_of_number <= 6:
        if scale_of_number <= 2:
            masked = "*" * scale_of_number
        else:
            masked = "*" * 2 + " " + "*" * (scale_of_number - 2)
    else:
        masked = " ".join(
            [refactored_card_number[:4], refactored_card_number[4:6] + "**", "****", refactored_card_number[-4:]]
        )

    logger.info(f"Маскирован номер карты: {masked}")
    return masked


def get_mask_account(card_number: int) -> str:
    """Функция маскировки номера банковского счета"""
    if card_number is None:
        logger.warning("Передано пустое значение номера счета.")
        return ""

    refactored_card_number = str(card_number)
    length = len(refactored_card_number)

    if length > 4:
        masked = "**" + refactored_card_number[-4:]
    else:
        if length == 1:
            masked = "*"
        else:
            visible_length = length - 2
            visible_digits = refactored_card_number[-visible_length:] if visible_length > 0 else ""
            masked = "**" + visible_digits

    logger.info(f"Маскирован номер счета: {masked}")
    return masked
