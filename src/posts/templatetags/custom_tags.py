from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag
def form_general(form):
    return render_to_string('form_general.html', {'form': form})
