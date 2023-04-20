from django.test import TestCase
from schema import Schema
from users.models import User


class BaseTestCase(TestCase):
    user_password = 'password!2'
    
    def generic_test(
        self,
        path: str,
        method: str,
        expected_status_code: int,
        expected_schema: Schema,
        **data,
    ) -> dict:
        '''
        - path
            request path
        - method
            request method
        - expected_status_code
            예상되는 결과의 상태 코드
        - expected_schema
            예상되는 결과의 스키마
        
        return: response json data
        '''

        request = getattr(self.client, method)
        res = request(
            path,
            data=data,
        )
        self.assertEqual(expected_status_code, res.status_code)

        if expected_status_code == 204:
            return {}
        
        res_data = res.json()
        self.assertTrue(expected_schema.is_valid(res_data))
        return res_data

    @classmethod
    def create_user(cls, **kwargs):
        user_kwargs = {
            'phone': '01012345678',
            'password': cls.user_password
        }
        user_kwargs.update(kwargs)
        return User.objects.create_user(**user_kwargs)
