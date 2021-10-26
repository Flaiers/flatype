from django.contrib.auth.models import AbstractUser, Permission, Group
from django.contrib.admin.models import LogEntry

from django.conf import settings
from django.db import models


class ProxyGroup(Group):

    class Meta:
        app_label = 'ext_auth'
        db_table = 'groups'
        proxy = True
        verbose_name = 'group'
        verbose_name_plural = 'groups'


class ProxyLogEntry(LogEntry):

    class Meta:
        app_label = 'admin'
        db_table = 'admin_log'
        proxy = True
        verbose_name = 'Admin log object'
        verbose_name_plural = 'Admin logs'


class User(AbstractUser):

    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField('email address', blank=True, null=True)
    link = models.URLField('user link', max_length=200, blank=True, null=True,
                           help_text='150 characters or fewer. Link to account on the site.')

    groups = models.ManyToManyField(Group, db_table='user_groups', blank=True,
                                    help_text='The groups this user belongs to. '
                                    'A user will get all permissions granted to each of their groups.',
                                    related_name='user_set', related_query_name='user')

    user_permissions = models.ManyToManyField(Permission, db_table='user_permissions', blank=True,
                                              help_text='Specific permissions for this user.',
                                              related_name='user_set', related_query_name='user')

    def save(self, *args, **kwargs):
        self.link = f'{settings.DOMAIN}/account/{self.username}'
        super(type(self), self).save(*args, **kwargs)


    class Meta(AbstractUser.Meta):
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
