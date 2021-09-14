
from django import forms

from django.contrib.auth.forms import (
    UserCreationForm as BaseUserCreationForm,
)
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class UserCreationForm(BaseUserCreationForm):
    email = forms.EmailField()

    class Meta(BaseUserCreationForm.Meta):
        model = UserModel
        fields = BaseUserCreationForm.Meta.fields + ('email',)
