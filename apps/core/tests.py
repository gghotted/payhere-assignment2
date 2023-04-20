from typing import Optional

from django.test import TestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from schema import Schema
from users.models import User


class BaseTestCase(TestCase):
    user_password = "password!2"

    def generic_test(
        self,
        path: str,
        method: str,
        expected_status_code: int,
        expected_schema: Schema,
        auth_user: Optional[User] = None,
        **data,
    ) -> dict:
        """
        - path
            request path
        - method
            request method
        - expected_status_code
            예상되는 결과의 상태 코드
        - expected_schema
            예상되는 결과의 스키마
        - auth_user
            인증 유저, 주어지면 access token을 header에 추가

        return: response json data
        """

        request = getattr(self.client, method)
        res = request(
            path,
            data=data,
            **self.get_auth_header(auth_user),
        )
        self.assertEqual(expected_status_code, res.status_code)

        if expected_status_code == 204:
            return {}

        res_data = res.json()
        self.assertTrue(expected_schema.is_valid(res_data))
        return res_data

    @classmethod
    def create_user(cls, **kwargs):
        user_kwargs = {"phone": "01012345678", "password": cls.user_password}
        user_kwargs.update(kwargs)
        return User.objects.create_user(**user_kwargs)

    @classmethod
    def create_token(cls, user):
        serializer = TokenObtainPairSerializer(
            data={
                "phone": user.phone,
                "password": cls.user_password,
            }
        )
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    @classmethod
    def get_auth_header(cls, user):
        if not user:
            return {}
        token = cls.create_token(user)
        return {"HTTP_AUTHORIZATION": f'Bearer {token["access"]}'}
