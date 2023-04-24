# Generated by Django 4.2 on 2023-04-21 17:31

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("stores", "0003_alter_category_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="생성 시간"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="수정 시간"),
                ),
                (
                    "price",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="가격",
                    ),
                ),
                (
                    "cost",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="원가",
                    ),
                ),
                ("name", models.CharField(max_length=32, verbose_name="이름")),
                ("chosung", models.CharField(max_length=32, verbose_name="초성")),
                ("description", models.TextField(verbose_name="설명")),
                ("barcode", models.CharField(max_length=16, verbose_name="바코드")),
                (
                    "sell_by_days",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="유통기한(일)",
                    ),
                ),
                (
                    "size",
                    models.CharField(
                        choices=[("small", "small"), ("large", "large")],
                        max_length=8,
                        verbose_name="사이즈",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="stores.category",
                        verbose_name="카테고리",
                    ),
                ),
                (
                    "store",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="stores.store",
                        verbose_name="매장",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "abstract": False,
            },
        ),
        migrations.AddConstraint(
            model_name="product",
            constraint=models.UniqueConstraint(
                fields=("store", "name"), name="unique_name_in_store"
            ),
        ),
    ]
