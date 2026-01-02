from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/')
async def root() -> dict[str, str]:
    logging.info("Запрос стартового ресурса...")
    return {'message': 'Hello World'}