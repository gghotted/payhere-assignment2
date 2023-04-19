from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name='생성 시간',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='수정 시간',
        auto_now=True,
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']
