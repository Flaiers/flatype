# Generated by Django 3.2.7 on 2021-09-14 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20210912_1839'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='text',
            new_name='content',
        ),
    ]
