from core.models import BaseModel
from django.core.validators import MinLengthValidator
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
        unique=True,
    )
