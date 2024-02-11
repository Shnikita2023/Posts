from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    """Кастомный менеджер для работы с БД"""
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Posts.Status.PUBLISHED)


class Posts(models.Model):
    """Модель постов"""

    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликована"

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(blank=True, verbose_name="Контент")
    photo = models.ImageField(upload_to="photo/%Y/%m/%d", default=None,
                              blank=True, null=True, verbose_name="Фото")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создание")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменение")
    is_published = models.BooleanField(choices=Status.choices,
                                       default=Status.PUBLISHED,
                                       verbose_name="Публикация")
    category = models.ForeignKey(to="Category",
                                 on_delete=models.CASCADE,
                                 related_name="posts",
                                 verbose_name="Тип категории")
    tag = models.ManyToManyField(to="TagPost",
                                 blank=True,
                                 related_name="tags",
                                 verbose_name="Теги")
    author = models.ForeignKey(get_user_model(),
                               related_name="posts",
                               verbose_name="Автор",
                               on_delete=models.SET_NULL,
                               default=None,
                               null=True)
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        db_table: str = "post"
        verbose_name: str = "Пост"
        verbose_name_plural: str = "Посты"
        ordering = ['-is_published']
        indexes = [
            models.Index(fields=['-is_published']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self) -> str:
        return reverse('post', kwargs={"post_slug": self.slug})


class Category(models.Model):
    """Модель категорий"""

    name = models.CharField(max_length=50, db_index=True, unique=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL")

    class Meta:
        db_table: str = "category"
        verbose_name: str = "Категория"
        verbose_name_plural: str = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self) -> str:
        return reverse('category', kwargs={"category_slug": self.slug})


class TagPost(models.Model):
    """Модель для связывания Постов и Тегов"""

    tag = models.CharField(max_length=100, db_index=True, verbose_name="Тег")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL")

    class Meta:
        db_table: str = "tag_post"
        verbose_name: str = "Тег пост"
        verbose_name_plural: str = "Тег постов"

    def __str__(self):
        return self.tag

    def get_absolute_url(self) -> str:
        return reverse('tag', kwargs={"tag_slug": self.slug})
