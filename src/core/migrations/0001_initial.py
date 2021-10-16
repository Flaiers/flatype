import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sessions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('author', models.CharField(blank=True, max_length=64, null=True)),
                ('content', models.TextField()),
                ('date', models.DateField(default=datetime.date.today)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('owner_sessions', models.ManyToManyField(blank=True, db_table='article_owners', to='sessions.Session')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
                'db_table': 'articles',
            },
        ),
    ]
