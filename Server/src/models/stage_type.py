"""
Модель типа этапа мероприятия.
"""

import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from models.db_session import db


class StageType(db, SerializerMixin):
    __tablename__ = 'stage_type'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String(32))

    def __repr__(self):
        return self.name
