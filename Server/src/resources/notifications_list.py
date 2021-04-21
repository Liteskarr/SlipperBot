"""
Данный ресурс призван дать возможность сторонним сервисам использовать напоминания.
Возвращает список пользователей, которые должны получить уведомление и сами уведомления.
"""

from collections import defaultdict
from datetime import datetime

from flask import jsonify
from flask_restful import Resource

from models.all_models import Group, Notification, Stage
from models.contest import Contest
from models.db_session import create_session


def get_result_template(last_id: int) -> dict:
    return {
        'meta': {'last_id': last_id},
        'contests': defaultdict(dict),
        'stages': defaultdict(dict),
        'students': defaultdict(list)
    }


def format_notification(notification: Notification) -> dict:
    return notification.to_dict(
        only=(
            'id',
            'date'
        )
    )


def format_stage(stage: Stage) -> dict:
    return stage.to_dict(
        only=(
            'name',
            'starting_date',
            'ending_date',
            'type',
            'description'
        )
    )


def format_contest(contest: Contest) -> dict:
    return contest.to_dict(
        only=(
            'name',
            'years',
            'type',
            'description'
        )
    )


def get_notifications(last_id: int):
    return create_session().query(Notification, Stage, Contest) \
        .join(Stage, Notification.stage_id == Stage.id) \
        .join(Contest, Stage.contest_id == Contest.id).filter(
        Notification.id > last_id,
        Notification.date < datetime.now(),
        Stage.ending_date > datetime.now()
    )


class NotificationsListResource(Resource):
    def get(self, last_id: int):
        session = create_session()
        result = get_result_template(last_id)
        notifications = get_notifications(last_id)
        for notification, stage, contest in notifications:
            result['meta']['last_id'] = max(result['meta']['last_id'], notification.id)
            for student in session.query(Group).get(notification.group_id).students:
                if contest.id in map(lambda x: x.id, student.declined_contests):
                    break
                if str(student.target_year) not in contest.years or not student.registered:
                    break
                result['students'][student.vk_id].append({
                    'notification': format_notification(notification),
                    'stage': stage.id,
                    'contest': contest.id
                })

        result['stages'] = dict(((stage.id, format_stage(stage))
                                 for stage in map(lambda x: x[1], notifications)))
        result['contests'] = dict(((contest.id, format_contest(contest))
                                   for contest in map(lambda x: x[2], notifications)))
        return jsonify(result)
