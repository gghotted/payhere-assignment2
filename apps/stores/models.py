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
