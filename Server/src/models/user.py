"""
Модель пользователя.
"""

import sqlalchemy
import sqlalchemy.orm as orm
from flask_login import UserMixin

from models.db_session import db


class User(db, UserMixin):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    login = sqlalchemy.Column(sqlalchemy.String(32))
    password_hash = sqlalchemy.Column(sqlalchemy.String)

    permission_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('permission.id'))
    permission = orm.relationship('Permission', backref='users')

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return self.login
