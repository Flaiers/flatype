from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm as BaseUserCreationForm,
)


UserModel = get_user_model()


class UserCreationForm(BaseUserCreationForm):

    class Meta(BaseUserCreationForm.Meta):
        model = UserModel
        fields = BaseUserCreationForm.Meta.fields + ('email',)
