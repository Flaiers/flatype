from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    link = models.URLField('User link', max_length=200, blank=True, null=True,
        help_text='150 characters or fewer. Link to account on the site.'
    )

    class Meta(AbstractUser.Meta):
        db_table = 'users'

