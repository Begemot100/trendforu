from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Profile, User


# Форма регистрации пользователя
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]


# Форма входа
class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


# Форма редактирования профиля (адрес и телефон)
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["address", "phone"]
        widgets = {
            "address": forms.TextInput(attrs={"placeholder": "Адрес доставки"}),
            "phone": forms.TextInput(attrs={"placeholder": "Телефон"}),
        }
