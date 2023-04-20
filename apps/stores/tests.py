from core.schemas import *
from core.tests import BaseTestCase
from django.urls import reverse_lazy

from stores.models import Store


class StoreCreateAPITestCase(BaseTestCase):
    path = reverse_lazy("my_stores:list")

    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()

    def test_url(self):
        self.assertEqual("/users/self/stores/", self.path)

    def test_success(self):
        """
        정상 생성
        """
        self.generic_test(
            self.path,
            "post",
            201,
            res201_schema(store_schema),
            auth_user=self.user,
            name="store",
        )

    def test_invalid_names(self):
        """
        유효하지 않은 이름
        """
        invalid_names = [
            "",  # blank
            "st",  # too short
            "s" * 33,  # too long,
        ]
        for name in invalid_names:
            self.generic_test(
                self.path,
                "post",
                400,
                res400_schema,
                auth_user=self.user,
                name=name,
            )

    def test_no_auth(self):
        """
        인증 없이
        """
        self.generic_test(
            self.path,
            "post",
            401,
            res401_schema,
        )


class StoreListAPITestCase(BaseTestCase):
    path = reverse_lazy("my_stores:list")

    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        stores = [Store(owner=cls.user, name="store%d" % i) for i in range(3)]
        cls.stores = Store.objects.bulk_create(stores)

    def test_url(self):
        self.assertEqual("/users/self/stores/", self.path)

    def test_success(self):
        """
        정상 조회
        """
        res = self.generic_test(
            self.path,
            "get",
            200,
            res200_schema(Schema([store_schema])),
            auth_user=self.user,
        )
        self.assertEqual(3, len(res["data"]))

    def test_no_auth(self):
        """
        인증 없이
        """
        self.generic_test(
            self.path,
            "get",
            401,
            res401_schema,
        )

    def test_filter_owner(self):
        """
        owner 필터링
        """
        new_user = self.create_user(phone="01087654321")
        res = self.generic_test(
            self.path,
            "get",
            200,
            res200_schema(Schema([store_schema])),
            auth_user=new_user,
        )
        self.assertEqual(0, len(res["data"]))
