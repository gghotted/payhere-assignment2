from core.models import BaseModel
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, phone, password):
        user = self.model(phone=phone)
        user.set_password(password)
        user.save()
        return user


class User(BaseModel, AbstractUser):
    username = None
    phone = models.CharField(
        verbose_name='휴대폰번호',
        unique=True,
        max_length=11,
        validators=[
            RegexValidator(
                r'^01[016789][0-9]{7,8}$',
                message='유효하지 않은 휴대폰번호 포맷입니다.',
            ),
        ]
    )

    objects = UserManager()
    
    USERNAME_FIELD = 'phone'
