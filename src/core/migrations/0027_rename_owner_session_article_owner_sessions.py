# Generated by Django 3.2.7 on 2021-09-16 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20210916_1558'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='owner_session',
            new_name='owner_sessions',
        ),
    ]
