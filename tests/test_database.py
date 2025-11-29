
import pytest
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def test_db():
    # Создание тестовой базы
    engine = create_engine("sqlite:///:memory:")
    
    # Применение миграций
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", "sqlite:///:memory:")
    
    with engine.begin() as connection:
        alembic_cfg.attributes['connection'] = connection
        command.upgrade(alembic_cfg, "head")
    
    yield engine
    engine.dispose()