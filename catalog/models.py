from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="наименование")
    description = models.TextField(verbose_name="описание", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = [
            "name",
        ]


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="наименование")
    description = models.TextField(verbose_name="описание", null=True, blank=True)
    image = models.ImageField(upload_to="media", verbose_name="изображение", null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    price = models.BigIntegerField(verbose_name="цена")
    created_at = models.DateField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateField(auto_now=True, verbose_name="дата последнего изменения", null=True)
    views_counter = models.PositiveIntegerField(verbose_name="Счетчик просмотров",
                                                help_text="Укажите количество просмотров", default=0)
    owner = models.ForeignKey(User, verbose_name="Владелец", help_text="Укажите владельца продукта", null=True,
                              blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["name"]
        permissions = [
            ("can_edit_name", "Can edit name"),
            ("can_edit_description", "Can edit description")
        ]
