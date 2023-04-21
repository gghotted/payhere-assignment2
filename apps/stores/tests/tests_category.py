from core.schemas import *
from core.tests import BaseTestCase
from django.urls import reverse
from stores.models import Store


class CategoryCreateAPITestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.store = Store.objects.create(owner=cls.user, name="store")
        cls.path = reverse("stores:list_category", args=[cls.store.id])

    def test_url(self):
        self.assertEqual("/stores/%d/categories/" % self.store.id, self.path)

    def test_success(self):
        """
        정상 생성
        """
        self.generic_test(
            self.path,
            "post",
            201,
            res201_schema(category_schema),
            auth_user=self.user,
            name="category",
        )

    def test_invalid_names(self):
        """
        유효하지 않은 이름
        """
        invalid_names = [
            None,
            "",
            "c" * 17,
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

    def test_duplicated_name(self):
        """
        중복 이름
        """
        self.test_success()
        self.generic_test(
            self.path,
            "post",
            400,
            res400_schema,
            auth_user=self.user,
            name="category",
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

    def test_not_owner(self):
        """
        owner가 아닌
        """
        new_user = self.create_user(phone="01098765432")
        self.generic_test(
            self.path,
            "post",
            403,
            res403_schema,
            auth_user=new_user,
        )
