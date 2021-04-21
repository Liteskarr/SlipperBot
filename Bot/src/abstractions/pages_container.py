"""
Отвечает за хранение пользовательских страниц.
"""

import sqlalchemy
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    vk_id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, index=True, unique=True, nullable=False)
    page_blob = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=False)


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


class PagesContainer:
    def __init__(self, database: str):
        self._database = database
        global_init(self._database)

    @staticmethod
    def contains(key: str):
        session = create_session()
        return session.query(User).filter_by(vk_id=key).first() is not None

    @staticmethod
    def get(key: str):
        session = create_session()
        user = session.query(User).get(key)
        if user is None:
            return None
        return user.page_blob

    @staticmethod
    def set(key: str, blob: bytes):
        session = create_session()
        user = session.query(User).get(key)
        if user is None:
            session.add(User(vk_id=key, page_blob=blob))
        else:
            user.page_blob = blob
        session.commit()
