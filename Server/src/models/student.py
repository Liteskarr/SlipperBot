"""
Модель студента.
"""

import json

import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy_serializer import SerializerMixin

import models.db_session as db_session
from models.db_session import db
from models.student_to_subject import student_to_subject


class Student(db, SerializerMixin):
    __tablename__ = 'student'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    vk_id = sqlalchemy.Column(sqlalchemy.String, index=True)

    name = sqlalchemy.Column(sqlalchemy.String(64))

    region = sqlalchemy.Column(sqlalchemy.Integer)

    current_year = sqlalchemy.Column(sqlalchemy.Integer)
    target_year = sqlalchemy.Column(sqlalchemy.Integer)

    registered = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    groups = orm.relationship('Group', secondary='student_to_group')

    subjects = orm.relationship('Subject', secondary='student_to_subject')

    declined_contests = orm.relationship('Contest', secondary='student_declines')

    def apply_json_args(self, args: dict):
        if args['vk_id'] is not None:
            self.vk_id = args['vk_id']
        if args['name'] is not None:
            self.name = args['name']
        if args['region'] is not None:
            self.region = args['region']
        if args['current_year'] is not None:
            self.current_year = args['current_year']
        if args['target_year'] is not None:
            self.target_year = args['target_year']
        if args['registered'] is not None:
            self.registered = args['registered']
        if args['subjects'] is not None:
            args['subjects'] = json.loads(args['subjects'].replace("'", '"'))
            for subject in args['subjects']:
                insertion = student_to_subject.insert().values(student_id=self.id,
                                                               subject_id=subject['id'])
                db_session.engine.execute(insertion)
        return self

    def __repr__(self):
        return f'Student<{self.id}> {self.name}'
