import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django import forms


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ("username", "password")


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ("username",
                  "password1",
                  "password2",
                  "first_name",
                  "last_name",
                  "email",
                  "photo",
                  "birth")
        labels = {
            "email": "E-mail",
            "first_name": "Имя",
            "last_name": "Фамилия"
        }

    def clean_email(self):
        email = self.cleaned_data["email"]

        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой email уже существует")

        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label="Логин")
    email = forms.EmailField(disabled=True, label="E-mail")
    this_year = datetime.date.today().year
    birth = forms.DateField(label="Дата рождения",
                            widget=forms.SelectDateWidget(years=tuple(range(this_year - 100, this_year - 5))))

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name", "photo", "birth")
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия"
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Cтарый пароль",
        widget=forms.PasswordInput())
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput())
    new_password2 = forms.CharField(
        label="Подтверждение нового пароля",
        widget=forms.PasswordInput())
