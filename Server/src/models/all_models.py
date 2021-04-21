"""
Модуль, содержащий все модели.
"""

from models.subject import Subject
from models.group import Group
from models.student import Student
from models.user import User
from models.permission import Permission
from models.notification import Notification
from models.stage import Stage
from models.stage_type import StageType
from models.contest_type import ContestType
from models.contest import Contest

from models.student_to_group import student_to_group
from models.student_to_subject import student_to_subject
from models.student_declines import student_declines
