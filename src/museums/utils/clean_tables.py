import logging

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import sessionmaker

from museums.engines import sqldb  # type: ignore  [import-untyped]

logger = logging.getLogger(__name__)


class CleanTables:

    def __init__(self, tables: list):
        self.tables = tables

    def clean(self) -> None:
        Session = sessionmaker(bind=sqldb.engine)
        for table in self.tables:
            session = Session()
            if session.query(table).first():
                try:
                    session.query(table).delete()
                    session.commit()
                    logging.info(f"Записи в таблице {table} удалены...")
                except DBAPIError as e:
                    session.rollback()
                    logging.info(f"Error: {e}, Ошибка удаления записей, откатываем транзакцию...")
            else:
                logging.info(f"Записи в таблице {table} отсутствуют...")
            session.close()
