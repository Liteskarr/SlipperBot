"""
Список отказов студентов от получения уведомлений.
"""

import sqlalchemy

from models.db_session import db


student_declines = sqlalchemy.Table(
    'student_declines',
    db.metadata,
    sqlalchemy.Column('student_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('student.id')),
    sqlalchemy.Column('contest_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('contest.id')),
    extend_existing=True
)
