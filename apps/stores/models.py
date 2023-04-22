from core.models import BaseModel
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models


class Store(BaseModel):
    owner = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="stores",
        verbose_name="소유자",
    )
    name = models.CharField(
        verbose_name="이름",
        max_length=32,
        validators=[MinLengthValidator(3)],
    )


class Category(BaseModel):
    store = models.ForeignKey(
        to=Store,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="매장",
    )
    name = models.CharField(
        verbose_name="이름",
        max_length=16,
    )


class Product(BaseModel):
    store = models.ForeignKey(
        to=Store,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="매장",
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="카테고리",
    )
    price = models.IntegerField(
        verbose_name="가격",
        validators=[MinValueValidator(0)],
    )
    cost = models.IntegerField(
        verbose_name="원가",
        validators=[MinValueValidator(0)],
    )
    name = models.CharField(
        verbose_name="이름",
        max_length=32,
    )
    chosung = models.CharField(
        verbose_name="초성",
        max_length=32,
    )
    description = models.TextField(
        verbose_name="설명",
    )
    barcode = models.CharField(
        verbose_name="바코드",
        max_length=16,
    )
    sell_by_days = models.IntegerField(
        verbose_name="유통기한(일)",
        validators=[MinValueValidator(0)],
    )
    size = models.CharField(
        verbose_name="사이즈",
        max_length=8,
        choices=[
            ("small", "small"),
            ("large", "large"),
        ],
    )

    class Meta(BaseModel.Meta):
        abstract = False
        constraints = [
            models.UniqueConstraint(
                fields=["store", "name"],
                name="unique_name_in_store",
            ),
        ]
