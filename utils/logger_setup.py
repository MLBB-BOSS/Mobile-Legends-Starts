# utils/logger_setup.py

import logging

def setup_logger(name: str) -> logging.Logger:
    """
    Налаштовує та повертає логгер з заданим ім'ям.

    :param name: Ім'я логгера.
    :return: Налаштований логгер.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
