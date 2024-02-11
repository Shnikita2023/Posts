from django.core.exceptions import ValidationError
from django import forms

from .models import Posts, Category


class AddPostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label="Без категорий",
                                      label="Тип категории")
    title = forms.CharField(min_length=5)

    class Meta:
        model = Posts
        fields = ("title", "slug", "content", "photo", "is_published", "category", "tag")

    def clean_title(self) -> str:
        title: str = self.cleaned_data.get("title")
        alphabet_rus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя "
        allowed = alphabet_rus + alphabet_rus.upper()

        if not (set(title) <= set(allowed)):
            raise ValidationError(message="Только русские буквы")

        return title


class AddFeedbackForm(forms.Form):
    name = forms.CharField(min_length=5, label="Имя")
    email = forms.EmailField(label="E-mail")
    message = forms.CharField(widget=forms.Textarea(),
                              label="Сообщение",
                              min_length=5)
