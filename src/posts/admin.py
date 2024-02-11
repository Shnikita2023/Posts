from typing import Literal

from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from posts.models import Posts, Category, TagPost


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    fields = ["title", "content", "photo", "post_photo", "slug", "is_published", "category", "tag"]
    list_display = ("id", "title", "time_create", "post_photo", "is_published", "category")
    list_display_links = ("id", "title")
    readonly_fields = ["post_photo"]
    ordering = ("time_create", "title")
    prepopulated_fields: dict[str, tuple[Literal["title"]]] = {"slug": ("title",)}
    list_per_page = 5
    actions = ("set_published_true", "set_published_false")
    search_fields = ("title",)
    list_filter = ("category__name", "is_published")
    save_on_top = True

    @admin.display(description="Изображение")
    def post_photo(self, post: Posts):
        """Добавление кастомного поля в админ-панель"""
        if post.photo:
            return mark_safe(f"<img src='{post.photo.url}' width=50>")

        return "Без фото"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published_true(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f"Изменено {count} записей")

    @admin.action(description="Снять c публикации выбранные записи")
    def set_published_false(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f"Изменено {count} записей", messages.WARNING)


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields: dict[str, tuple[Literal["name"]]] = {"slug": ("name",)}


@admin.register(TagPost)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields: dict[str, tuple[Literal["name"]]] = {"slug": ("tag",)}
