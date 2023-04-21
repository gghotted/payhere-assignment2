from operator import attrgetter

from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    obj의 owner와 request user가 일치하는지 체크합니다
    owner_id_field를 통해 obj에서 user id를 가져옵니다
    ex)
        owner_id_field 가 "parent.owner_id" 라면
        obj.parent.owner_id와 request.user.id를 비교합니다
    """

    def __init__(self, owner_id_field: str):
        self.owner_id_field = owner_id_field

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_authenticated and user.id == attrgetter(self.owner_id_field)(obj)
