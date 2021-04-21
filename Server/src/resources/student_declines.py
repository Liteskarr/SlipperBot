"""
Ресурс, предоставляющий доступ к данным о студенческих отказах о мероприятиях.
"""

from flask_restful import Resource
from flask_restful.reqparse import RequestParser

import models.db_session as db_session
from models.all_models import student_declines, Student

parser = RequestParser()
parser.add_argument('contest_id', type=int)


class StudentDeclinesResource(Resource):
    def post(self, vk_id: str):
        args = parser.parse_args()
        if args['contest_id'] is None:
            return 409
        session = db_session.create_session()
        student_id = session.query(Student).filter(Student.vk_id == vk_id).first().id
        inserting = student_declines.insert().values(student_id=student_id,
                                                     contest_id=args['contest_id'])
        db_session.engine.execute(inserting)
        return 200

    def delete(self, vk_id: str):
        args = parser.parse_args()
        if args['contest_id'] is None:
            return 409
        session = db_session.create_session()
        student_id = session.query(Student).filter(Student.vk_id == vk_id).first().id
        deleting = student_declines.delete().where(student_id=student_id,
                                                   contest_id=args['contest_id'])
        db_session.engine.execute(deleting)
        return 200
