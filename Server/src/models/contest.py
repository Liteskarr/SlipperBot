"""
Модуль, содержащий модель мероприятия.
"""

import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy_serializer import SerializerMixin

from models.db_session import db


class Contest(db, SerializerMixin):
    __tablename__ = 'contest'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String(64))

    years = sqlalchemy.Column(sqlalchemy.String)

    type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('contest_type.id'))
    type = orm.relation('ContestType')

    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('subject.id'))
    subject = orm.relation('Subject')

    description = sqlalchemy.Column(sqlalchemy.Text)

    def get_years(self) -> list:
        return self.years.split(';')

    def add_year(self, year: str):
        years = self.years.split(';')
        years.append(year)
        years.sort()
        self.years = ';'.join(years)

    def delete_year(self, year: str):
        years = self.years.split(';')
        if year not in years:
            return
        years.remove(year)
        self.years = ';'.join(years)

    def __repr__(self):
        return f'<{self.id}> {self.name}'
