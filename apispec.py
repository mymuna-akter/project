from resources import UserResource, ParentIdResource, UserInfo, ChildIdResource, ParentResource, ChildResource


def configure_apispec(api):
    api.add_resource(UserResource, '/user')
    api.add_resource(ParentIdResource, '/parent-ids')
    api.add_resource(ChildIdResource, '/child-ids')
    api.add_resource(ParentResource, '/parent/<int:parent_id>')
    api.add_resource(ChildResource, '/child/<int:child_id>')

    api.add_resource(UserInfo, '/user/<int:user_id>')
