from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app import app
from models.all_models import *
from models.db_session import create_session


class MyView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated


def init():
    session = create_session()
    admin = Admin(app, index_view=MyView())
    admin.add_view(ModelView(Contest, session))
    admin.add_view(ModelView(Stage, session))
    admin.add_view(ModelView(Group, session))
    admin.add_view(ModelView(Student, session))
    admin.add_view(ModelView(Notification, session))
    admin.add_view(ModelView(Subject, session))
    admin.add_view(ModelView(StageType, session))
    admin.add_view(ModelView(ContestType, session))
    admin.add_view(ModelView(User, session))
    admin.add_view(ModelView(Permission, session))
