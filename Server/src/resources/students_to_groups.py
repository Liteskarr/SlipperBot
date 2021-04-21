"""
Ресурс, предоставляющий доступ к связям студентов и преподавательских групп.
"""

from flask import jsonify
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

import models.db_session as db_session
from models.all_models import student_to_group
from models.db_session import create_session

parser = RequestParser()
parser.add_argument('student_id', type=int)
parser.add_argument('group_id', type=int)


class StudentsToGroupsResource(Resource):
    def get(self):
        result = []
        for row in create_session().query(student_to_group).all():
            result.append({
                'student_id': row[0],
                'group_id': row[1]
            })
        return jsonify(result)

    def post(self):
        global engine
        args = parser.parse_args()
        if args['student_id'] is None or args['group_id'] is None:
            return 409
        inserting = student_to_group.insert().values(student_id=args['student_id'], group_id=args['group_id'])
        db_session.engine.execute(inserting)
        return 200

    def delete(self):
        args = parser.parse_args()
        if args['student_id'] is None or args['group_id'] is None:
            return 409
        deleting = student_to_group.delete().where(student_to_group.c.student_id == args['student_id'],
                                                   student_to_group.c.group_id == args['group_id'])
        db_session.engine.execute(deleting)
        return 200
