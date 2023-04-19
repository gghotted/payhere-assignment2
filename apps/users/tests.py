from core.schemas import *
from django.test import TestCase
from django.urls import reverse_lazy


class UserCreateAPITestCase(TestCase):
    path = reverse_lazy('users:create')

    def test_url(self):
        self.assertEqual('/users/', self.path)

    def _test_create(
        self,
        phone='01012345678',
        password='password!2',
        password2='password!2',
        expected_status_code=201,
        expected_schema=res201_schema(user_schema),
    ):
        res = self.client.post(
            self.path,
            data={
                'phone': phone,
                'password': password,
                'password2': password2,
            }
        )
        self.assertEqual(expected_status_code, res.status_code)
        self.assertTrue(expected_schema.is_valid(res.json()))

    def test_success(self):
        '''
        정상 생성
        '''
        self._test_create()

    def test_password_mismatch(self):
        '''
        비밀번호 불일치
        '''
        self._test_create(password2='password!1', expected_status_code=400, expected_schema=res400_schema)

    def test_already_exists_phone(self):
        '''
        휴대폰번호 중복 체크
        '''
        self._test_create()
        self._test_create(expected_status_code=400, expected_schema=res400_schema)

    def test_phone_format_invalid(self):
        '''
        휴대폰번호 포맷 체크
        '''
        invalid_list = [
            '010 1234 5678', # space
            '010-1234-5678', # hyphen
            '010123456', # too short
            '010123456789', # too long
            '01412345678', # wrong prefix
        ]
        for phone in invalid_list:
            self._test_create(phone=phone, expected_status_code=400, expected_schema=res400_schema)
