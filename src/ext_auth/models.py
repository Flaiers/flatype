from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    link = models.URLField('User link', max_length=200, blank=True, null=True,
        help_text='150 characters or fewer. Link to account on the site.'
    )

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'


UserModel = get_user_model()


class ExternalHashId(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    session = models.CharField(max_length=32, unique=True, blank=True, null=True, db_index=True)

    class Meta:
        db_table = 'auth_hash'
        verbose_name = "External hash id"
        verbose_name_plural = "External hash id's"
