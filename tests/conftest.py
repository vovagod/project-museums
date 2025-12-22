import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session


class Base(DeclarativeBase):

    pass


@pytest.fixture
def test_engine():

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def test_session(test_engine):

    Session = scoped_session(sessionmaker(bind=test_engine))
    session = Session()
    yield session
    session.close()


@pytest.fixture
def test_db(test_engine):  # development, настроить!

    alembic_cfg = Config("alembic.ini")
    print(f"alembic_cfg: {alembic_cfg}")
    alembic_cfg.set_main_option("sqlalchemy.url", "sqlite:///:memory:")
    with test_engine.begin() as connection:
        alembic_cfg.attributes['connection'] = connection
        command.upgrade(alembic_cfg, "head")
    yield test_engine
    test_engine.dispose()
