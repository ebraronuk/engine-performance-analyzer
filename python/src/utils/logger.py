"""
Basit logger kurulumu.
INFO seviyesinde konsola yazar.
"""

import logging
from typing import Optional


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Modul veya uygulama icin logger dondurur.

    Parametreler:
        name: Logger adi (None ise root kullanilir).

    Döndürür:
        logging.Logger ornegi.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Tek seferlik handler ekle
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger
