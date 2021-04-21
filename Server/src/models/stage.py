"""
Модель этапа мероприятия.
"""

import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy_serializer import SerializerMixin

from models.db_session import db


class Stage(db, SerializerMixin):
    __tablename__ = 'stage'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String(32))

    starting_date = sqlalchemy.Column(sqlalchemy.DateTime)
    ending_date = sqlalchemy.Column(sqlalchemy.DateTime)

    type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('stage_type.id'))
    type = orm.relationship('StageType')

    contest_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('contest.id'))
    contest = orm.relationship('Contest', backref=orm.backref('stages', lazy=True))

    description = sqlalchemy.Column(sqlalchemy.Text)

    remote = sqlalchemy.Column(sqlalchemy.Boolean)

    def __repr__(self):
        return f'<{self.id}> {self.name}'
