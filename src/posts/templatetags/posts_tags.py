from django import template
from django.db.models import Count

from posts.models import Category, TagPost

register = template.Library()


@register.inclusion_tag("posts/list_categories.html")
def show_all_categories(category_selected: int = 0) -> dict:
    categories = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)
    return {'categories': categories, 'category_selected': category_selected}


@register.inclusion_tag("posts/list_tags.html")
def show_all_tags() -> dict:
    return {'tags': TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}
