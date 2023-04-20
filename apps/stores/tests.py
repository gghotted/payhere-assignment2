from core.schemas import *
from core.tests import BaseTestCase
from django.urls import reverse, reverse_lazy

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


class StoreRetrieveAPITestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.store = Store.objects.create(owner=cls.user, name="store")
        cls.path = reverse("stores:detail", args=[cls.store.id])

    def test_url(self):
        self.assertEqual("/stores/%d/" % self.store.id, self.path)

    def test_success(self):
        """
        정상 조회
        """
        self.generic_test(
            self.path,
            "get",
            200,
            res200_schema(store_schema),
            auth_user=self.user,
        )

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

    def test_not_owner(self):
        """
        owner가 아닌
        """
        new_user = self.create_user(phone="01098765432")
        self.generic_test(
            self.path,
            "get",
            403,
            res403_schema,
            auth_user=new_user,
        )


class StoreUpdateAPITestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.store = Store.objects.create(owner=cls.user, name="store")
        cls.path = reverse("stores:detail", args=[cls.store.id])

    def test_url(self):
        self.assertEqual("/stores/%d/" % self.store.id, self.path)

    def test_success(self):
        """
        정상 수정
        """
        new_name = "updated name"
        self.generic_test(
            self.path,
            "patch",
            200,
            res200_schema(store_schema),
            auth_user=self.user,
            name=new_name,
        )
        store = Store.objects.get(id=self.store.id)
        self.assertEqual(new_name, store.name)

    def test_no_auth(self):
        """
        인증 없이
        """
        self.generic_test(
            self.path,
            "patch",
            401,
            res401_schema,
        )

    def test_not_owner(self):
        """
        owner가 아닌
        """
        new_user = self.create_user(phone="01098765432")
        self.generic_test(
            self.path,
            "patch",
            403,
            res403_schema,
            auth_user=new_user,
        )
