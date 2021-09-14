# Generated by Django 3.2.7 on 2021-09-12 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ext_auth', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ExternalHashId',
            new_name='ExternalSession',
        ),
        migrations.AlterModelOptions(
            name='externalsession',
            options={'verbose_name': 'External session', 'verbose_name_plural': 'External sessions'},
        ),
        migrations.AlterModelTable(
            name='externalsession',
            table='external_sessions',
        ),
        migrations.AlterModelTable(
            name='user',
            table='users',
        ),
    ]