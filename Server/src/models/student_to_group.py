"""
Список связей между студентами и группами.
"""

import sqlalchemy
from models.db_session import db


student_to_group = sqlalchemy.Table(
    'student_to_group',
    db.metadata,
    sqlalchemy.Column('student_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('student.id')),
    sqlalchemy.Column('group_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('group.id')),
    extend_existing=True
)