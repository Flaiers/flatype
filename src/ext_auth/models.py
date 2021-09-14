from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField('email address', blank=True, null=True)
    link = models.URLField('user link', max_length=200, blank=True, null=True,
                           help_text='150 characters or fewer. Link to account on the site.')

    class Meta(AbstractUser.Meta):
        db_table = 'users'
