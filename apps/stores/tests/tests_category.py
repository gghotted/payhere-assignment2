from core.schemas import *
from core.tests import BaseTestCase
from django.urls import reverse
from stores.models import Category, Store


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

        queries 4개:
            1. get user (request user),
            2. get store (permission check를 위해)
            3. check unique category name
            4. insert category
        """
        self.generic_test(
            self.path,
            "post",
            201,
            res201_schema(category_schema),
            expected_query_count=4,
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


class CategoryListAPITestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.store = Store.objects.create(owner=cls.user, name="store")
        cls.path = reverse("stores:list_category", args=[cls.store.id])

        Category.objects.bulk_create(
            Category(store=cls.store, name="name%d" % i) for i in range(3)
        )

    def test_url(self):
        self.assertEqual("/stores/%d/categories/" % self.store.id, self.path)

    def test_success(self):
        """
        정상 조회
        """
        res = self.generic_test(
            self.path,
            "get",
            200,
            res200_schema(Schema([category_schema])),
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

    def test_filter_by_store(self):
        """
        store에 해당하는 category만 리스팅 되는지
        """
        store = Store.objects.create(owner=self.user, name="store2")
        Category.objects.create(store=store, name="name")
        self.test_success()


class CategoryRetrieveAPITestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.store = Store.objects.create(owner=cls.user, name="store")
        cls.category = Category.objects.create(store=cls.store, name="category")
        cls.path = reverse(
            "stores:detail_category", args=[cls.store.id, cls.category.id]
        )

    def test_url(self):
        path = "/stores/%d/categories/%d/" % (self.store.id, self.category.id)
        self.assertEqual(path, self.path)

    def test_success(self):
        """
        정상 조회
        """
        self.generic_test(
            self.path,
            "get",
            200,
            res200_schema(category_schema),
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

    def test_not_found_store(self):
        path = reverse("stores:detail_category", args=[42, self.category.id])
        self.generic_test(
            path,
            "get",
            404,
            res404_schema,
            auth_user=self.user,
        )


class CategoryUpdateAPITestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.store = Store.objects.create(owner=cls.user, name="store")
        cls.category = Category.objects.create(store=cls.store, name="category")
        cls.path = reverse(
            "stores:detail_category", args=[cls.store.id, cls.category.id]
        )

    def test_url(self):
        path = "/stores/%d/categories/%d/" % (self.store.id, self.category.id)
        self.assertEqual(path, self.path)

    def test_success(self):
        """
        정사 수정
        """
        self.generic_test(
            self.path,
            "patch",
            200,
            res200_schema(category_schema),
            auth_user=self.user,
            name="updated_name",
        )
        category = Category.objects.get(id=self.category.id)
        self.assertEqual("updated_name", category.name)

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


class CategoryDeleteAPITestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.store = Store.objects.create(owner=cls.user, name="store")
        cls.category = Category.objects.create(store=cls.store, name="category")
        cls.path = reverse(
            "stores:detail_category", args=[cls.store.id, cls.category.id]
        )

    def test_url(self):
        path = "/stores/%d/categories/%d/" % (self.store.id, self.category.id)
        self.assertEqual(path, self.path)

    def test_success(self):
        """
        정상 삭제
        """
        self.generic_test(
            self.path,
            "delete",
            204,
            expected_schema=None,
            auth_user=self.user,
        )

    def test_no_auth(self):
        """
        인증 없이
        """
        self.generic_test(
            self.path,
            "delete",
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
            "delete",
            403,
            res403_schema,
            auth_user=new_user,
        )
