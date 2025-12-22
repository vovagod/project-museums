import logging
import os
from logging.config import dictConfig
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = ""
    DB_PORT: int = 0
    DB_NAME: str = ""
    DB_BASE: str = ""
    DB_BASE_ASYNC: str = ""

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(env_file=os.path.join(BASE_DIR, ".env"))


settings: "Settings" = Settings()

LOGGING = {
    "version": 1,
    "formatters": {"default": {"format": "%(asctime)s %(levelname)-8s %(name)-15s %(message)s"}},
    "handlers": {
        "console": {"level": logging.INFO, "class": "logging.StreamHandler", "formatter": "default"},
        # "file": {
        # "level": logging.INFO,
        # "class": logging.handlers.RotatingFileHandler,
        # "formatter": "precise",
        # "filename": os.path.join(BASE_DIR, 'logs', 'debug.log'),
        # "maxBytes": 1024,
        # "backupCount": 3,
        # },
    },
    "loggers": {"": {"handlers": ["console"], "level": logging.INFO}},
}

# Создать директорию, если не существует
# log_dir = os.path.dirname(LOGGING['handlers']['file']['filename'])
# if not os.path.exists(log_dir):
# os.makedirs(log_dir, exist_ok=True)  # exist_ok=True avoids errors if the directory exists

dictConfig(LOGGING)
