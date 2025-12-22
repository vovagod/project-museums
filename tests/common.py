import os
from sqlalchemy import orm

Session = orm.scoped_session(orm.sessionmaker())
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
