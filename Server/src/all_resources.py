from app import rest_api, api_prefix
from resources.notifications_list import NotificationsListResource
from resources.student import StudentResource
from resources.student_declines import StudentDeclinesResource
from resources.students_to_groups import StudentsToGroupsResource
from resources.subjects_list import SubjectsListResource


def init_all():
    rest_api.add_resource(SubjectsListResource, api_prefix + '/subjects/')
    rest_api.add_resource(StudentResource, api_prefix + '/student/<string:vk_id>')
    rest_api.add_resource(NotificationsListResource, api_prefix + '/notifications/<int:last_id>')
    rest_api.add_resource(StudentsToGroupsResource, api_prefix + '/students_to_groups/')
    rest_api.add_resource(StudentDeclinesResource, api_prefix + '/student_declines/<string:vk_id>')
