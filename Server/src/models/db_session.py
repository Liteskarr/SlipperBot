"""
Модуль, содержащий все необходимое для работы с sqlalchemy.
"""

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

db = dec.declarative_base()

__factory = None
engine = None


def global_init(db_file):
    global __factory, engine

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from models import all_models

    db.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
