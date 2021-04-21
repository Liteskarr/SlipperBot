"""
Модуль, содержащий модель уведомления.
"""

import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy_serializer import SerializerMixin

from models.db_session import db


class Notification(db, SerializerMixin):
    __tablename__ = 'notification'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    date = sqlalchemy.Column(sqlalchemy.DateTime)

    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('group.id'))
    group = orm.relationship('Group', backref=orm.backref('notifications', lazy=True))

    stage_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('stage.id'))
    stage = orm.relationship('Stage', backref=orm.backref('notifications', lazy=True))
