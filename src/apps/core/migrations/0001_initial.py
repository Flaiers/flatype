import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('author', models.CharField(blank=True, max_length=64, null=True)),
                ('content', models.TextField()),
                ('date', models.DateField(default=datetime.date.today)),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
                'db_table': 'articles',
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(blank=True, db_index=True, max_length=255, null=True, unique=True)),
                ('use_hash', models.BooleanField(default=True)),
                ('file', models.FileField(db_index=True, unique=True, upload_to='')),
                ('date', models.DateField(default=datetime.date.today)),
            ],
            options={
                'verbose_name': 'Storage object',
                'verbose_name_plural': 'Storage',
                'db_table': 'storage',
            },
        ),
    ]
