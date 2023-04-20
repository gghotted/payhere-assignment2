from datetime import timedelta

from core.schemas import *
from core.tests import BaseTestCase
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from freezegun import freeze_time
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class UserCreateAPITestCase(BaseTestCase):
    path = reverse_lazy("users:create")

    def test_url(self):
        self.assertEqual("/users/", self.path)

    def test_success(self):
        """
        정상 생성
        """
        self.generic_test(
            self.path,
            "post",
            201,
            res201_schema(user_schema),
            phone="01012345678",
            password=self.user_password,
            password2=self.user_password,
        )

    def test_password_mismatch(self):
        """
        비밀번호 불일치
        """
        self.generic_test(
            self.path,
            "post",
            400,
            res400_schema,
            phone="01012345678",
            password=self.user_password,
            password2=self.user_password + "1",
        )

    def test_already_exists_phone(self):
        """
        휴대폰번호 중복 체크
        """
        data = {
            "phone": "01012345678",
            "password": self.user_password,
            "password2": self.user_password,
        }
        self.generic_test(self.path, "post", 201, res201_schema(user_schema), **data)
        self.generic_test(self.path, "post", 400, res400_schema, **data)

    def test_phone_format_invalid(self):
        """
        휴대폰번호 포맷 체크
        """
        invalid_list = [
            "010 1234 5678",  # space
            "010-1234-5678",  # hyphen
            "010123456",  # too short
            "010123456789",  # too long
            "01412345678",  # wrong prefix
        ]
        for phone in invalid_list:
            self.generic_test(
                self.path,
                "post",
                400,
                res400_schema,
                phone=phone,
                password=self.user_password,
                password2=self.user_password,
            )


class TokenCreateAPITestCase(BaseTestCase):
    path = reverse_lazy("auth:create_token")

    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()

    def test_url(self):
        self.assertEqual("/auth/tokens/", self.path)

    def test_success(self):
        """
        정상 생성
        """
        return self.generic_test(
            self.path,
            "post",
            200,
            res200_schema(token_schema),
            phone=self.user.phone,
            password=self.user_password,
        )

    def test_invalid_datas(self):
        """
        유효하지 않은 입력
        """
        invalid_datas = {
            "no_data": {},
            "no_phone": {"password": self.user_password},
            "no_password": {"phone": self.user.phone},
        }

        for data in invalid_datas.values():
            self.generic_test(
                self.path,
                "post",
                400,
                res400_schema,
                **data,
            )

    def test_mismatch_datas(self):
        """
        일치하는 유저 없음
        """
        mismatch_datas = {
            "mismatch_phone": {
                "phone": self.user.phone + "1",
                "password": self.user_password,
            },
            "mismatch_password": {
                "phone": self.user.phone,
                "password": self.user_password + "1",
            },
        }

        for data in mismatch_datas.values():
            self.generic_test(
                self.path,
                "post",
                401,
                res401_schema,
                **data,
            )

    def test_access_token_lifetime(self):
        """
        엑세스 토큰 유효 기간
        """
        time = now()
        with freeze_time(time):
            tokens = self.test_success()
        access = tokens["data"]["access"]

        lifetime = timedelta(hours=1)
        not_expired = lifetime - timedelta(seconds=1)
        expired = lifetime + timedelta(seconds=1)

        with freeze_time(time + not_expired):
            # not raise
            AccessToken(access)

        with freeze_time(time + expired):
            self.assertRaises(
                TokenError,
                AccessToken,
                access,
            )

    def test_refresh_token_lifetime(self):
        """
        리프레시 토큰 유효 기간
        """
        time = now()
        with freeze_time(time):
            tokens = self.test_success()
        refresh = tokens["data"]["refresh"]

        lifetime = timedelta(days=7)
        not_expired = lifetime - timedelta(seconds=1)
        expired = lifetime + timedelta(seconds=1)

        with freeze_time(time + not_expired):
            # not raise
            RefreshToken(refresh)

        with freeze_time(time + expired):
            self.assertRaises(
                TokenError,
                RefreshToken,
                refresh,
            )


class TokenRefreshAPITestCase(BaseTestCase):
    path = reverse_lazy("auth:refresh_token")

    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.token = cls.create_token(cls.user)

    def test_url(self):
        self.assertEqual("/auth/tokens/refresh/", self.path)

    def test_success(self):
        """
        정상 리프레시
        """
        self.generic_test(
            self.path,
            "post",
            200,
            res200_schema(Schema({"access": str})),
            refresh=self.token["refresh"],
        )


class TokenBlackListAPITestCase(BaseTestCase):
    path = reverse_lazy("auth:blacklist_token")

    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.token = cls.create_token(cls.user)

    def test_url(self):
        self.assertEqual("/auth/tokens/blacklist/", self.path)

    def test_success(self):
        """
        블랙리스트에 정상 등록
        """
        self.generic_test(
            self.path,
            "post",
            200,
            res200_schema(Schema({})),
            refresh=self.token["refresh"],
        )
        self.generic_test(
            reverse("auth:refresh_token"),
            "post",
            401,
            res401_schema,
            refresh=self.token["refresh"],
        )
