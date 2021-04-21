"""
Ресурс, предоставляющий доступ к списку предметов.
"""


from flask import jsonify
from flask_restful import Resource

from models.db_session import create_session
from models.all_models import Subject


class SubjectsListResource(Resource):
    def get(self):
        session = create_session()
        return jsonify({'subjects': [item.to_dict() for item in session.query(Subject).all()]})
