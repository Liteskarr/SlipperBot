"""
Список связей между студентами и предметами.
"""

import sqlalchemy

from models.db_session import db

student_to_subject = sqlalchemy.Table(
    'student_to_subject',
    db.metadata,
    sqlalchemy.Column('student_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('student.id')),
    sqlalchemy.Column('subject_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('subject.id')),
    extend_existing=True
)
