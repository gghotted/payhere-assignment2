from operator import attrgetter

from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    obj의 owner와 request user가 일치하는지 체크합니다
    owner_field를 통해 obj에서 user object를 가져옵니다
    ex)
        owner_field 가 "parent.owner" 라면
        obj.parent.owner와 request.user를 비교합니다
    """

    def __init__(self, owner_field: str):
        self.owner_field = owner_field

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_authenticated and user == attrgetter(self.owner_field)(obj)
