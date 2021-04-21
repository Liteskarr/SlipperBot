"""
Ресурс, предоставляющий доступ к данным студента.
"""

from flask import jsonify, abort
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from models.all_models import Student
from models.db_session import create_session

parser = RequestParser()
parser.add_argument('vk_id', type=str)
parser.add_argument('name', type=str)
parser.add_argument('region', type=int)
parser.add_argument('current_year', type=int)
parser.add_argument('target_year', type=int)
parser.add_argument('subjects')
parser.add_argument('registered', type=bool)


class StudentResource(Resource):
    def get(self, vk_id: str):
        session = create_session()
        student = session.query(Student).filter_by(vk_id=vk_id).first()
        if student is None:
            return abort(404)
        return jsonify(student.to_dict())

    def post(self, vk_id: str):
        session = create_session()
        student = session.query(Student).filter_by(vk_id=vk_id).first()
        if student is not None:
            return abort(409)
        args = parser.parse_args()
        try:
            student = Student().apply_json_args(args)
        except Exception:
            return abort(409)
        session.add(student)
        session.commit()
        return 200

    def put(self, vk_id: str):
        session = create_session()
        student = session.query(Student).filter_by(vk_id=vk_id).first()
        if student is None:
            return abort(409)
        args = parser.parse_args()
        student.apply_json_args(args)
        session.commit()
        return 200
