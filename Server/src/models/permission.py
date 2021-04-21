"""
Модель разрешения пользователя.
"""

import sqlalchemy
from models.db_session import db


class Permission(db):
    __tablename__ = 'permission'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String(32))

    level = sqlalchemy.Column(sqlalchemy.Integer)

    def __repr__(self):
        return self.name
