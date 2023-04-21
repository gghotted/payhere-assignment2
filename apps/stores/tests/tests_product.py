from core.schemas import *
from core.tests import BaseTestCase
from django.urls import reverse
from stores.models import Category, Store


class ProductCreateAPITestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.store = Store.objects.create(owner=cls.user, name="store")
        cls.category = Category.objects.create(store=cls.store, name="category")
        cls.path = reverse("stores:list_product", args=[cls.store.id])

    def setUp(self):
        self.data = {
            "category": self.category.id,
            "price": 5000,
            "cost": 3000,
            "name": "슈크림 라떼",
            "description": "맛있는 슈크림 라떼",
            "barcode": "1234567890",
            "sell_by_days": 3,
            "size": "small",
        }

    def test_url(self):
        self.assertEqual("/stores/%d/products/" % self.store.id, self.path)

    def test_success(self):
        """
        정상 생성

        queries 5개:
            1. get user (request user)
            2. get store (permission check)
            3. check category (validation check)
            4. check unique name (validation check)
            5. insert product
        """
        self.generic_test(
            self.path,
            "post",
            201,
            res201_schema(product_schema),
            expected_query_count=5,
            auth_user=self.user,
            **self.data,
        )

    def test_duplicated_name_in_same_store(self):
        """
        같은 매장에서 중복된 상품 이름
        """
        self.test_success()
        self.generic_test(
            self.path,
            "post",
            400,
            res400_schema,
            auth_user=self.user,
            **self.data,
        )

    def test_duplicated_name_in_another_store(self):
        """
        다른 매장에서 중복된 상품 이름
        """
        store = Store.objects.create(owner=self.user, name="store2")
        category = Category.objects.create(store=store, name="category")
        data = self.data.copy()
        data["category"] = category.id
        self.generic_test(
            reverse("stores:list_product", args=[store.id]),
            "post",
            201,
            res201_schema(product_schema),
            auth_user=self.user,
            **data,
        )

        """
        다른 매장에서 같은 이름의 상품이 있더라도, 정상 생성
        """
        self.test_success()

    def test_another_store_category(self):
        """
        다른 매장의 카테고리로 생성
        """
        store = Store.objects.create(owner=self.user, name="store2")
        category = Category.objects.create(store=store, name="category")
        self.data["category"] = category.id
        self.generic_test(
            self.path,
            "post",
            400,
            res400_schema,
            auth_user=self.user,
            **self.data,
        )

    def test_chosung(self):
        """
        parsing된 초성 체크
        """
        chosungs = {
            "슈크림 라떼": "ㅅㅋㄹ ㄹㄸ",
            "슈크림 라떼2": "ㅅㅋㄹ ㄹㄸ2",
            "슈크림 라떼X": "ㅅㅋㄹ ㄹㄸX",
        }
        for name, chosung in chosungs.items():
            self.data["name"] = name
            res = self.generic_test(
                self.path,
                "post",
                201,
                res201_schema(product_schema),
                auth_user=self.user,
                **self.data,
            )
            self.assertEqual(chosung, res["data"]["chosung"])

    def test_invalid_datas(self):
        """
        기타 유효하지 않은 인풋 데이터
        """
        invalid_datas = [
            {"category": 42},
            {"price": -1},
            {"cost": -1},
            {"name": "a" * 33},
            {"barcode": "a" * 17},
            {"sell_by_days": -1},
            {"size": "xlarge"},
        ]
        for data in invalid_datas:
            new_data = self.data.copy()
            new_data.update(data)
            self.generic_test(
                self.path, "post", 400, res400_schema, auth_user=self.user, **new_data
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
