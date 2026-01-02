from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
import logging

from . import config

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator:  # noqa: ARG001
    await startup()
    try:
        yield
    finally:
        await shutdown()


async def startup() -> None:
    show_config()
    # connect to the database
    logging.info("Старт приложения...")


async def shutdown() -> None:
    # disconnect from the database
    logging.info("Стоп приложения...")


def show_config() -> None:
    config_vars = {key: getattr(config, key) for key in sorted(dir(config)) if key.isupper()}
    logging.debug(f"Конфигурация: {config_vars}")