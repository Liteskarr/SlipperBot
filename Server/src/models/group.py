"""
Модуль, содержащий модель, описывающую преподавательскую группу.
"""

import sqlalchemy
import sqlalchemy.orm as orm

from models.db_session import db


class Group(db):
    __tablename__ = 'group'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String(32))

    admin_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'))
    admin = orm.relationship('User', backref=orm.backref('groups', lazy=True))

    students = orm.relationship('Student', secondary='student_to_group')

    def __repr__(self):
        return f'Group<{self.id}> {self.name}'
