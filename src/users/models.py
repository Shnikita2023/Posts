from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    photo = models.ImageField(
        upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фото"
    )
    birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")

    class Meta:
        db_table: str = "user"
        verbose_name: str = "Пользователь"
        verbose_name_plural: str = "Пользователи"

    def __str__(self):
        return self.username
