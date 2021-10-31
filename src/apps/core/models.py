from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model

from django.db.utils import IntegrityError

from django.utils.text import slugify

from packs import generate_data_hash

from django.conf import settings
from django.db import models

from datetime import date


UserModel = get_user_model()


class Article(models.Model):

    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, db_index=True, blank=True)
    author = models.CharField(max_length=64, null=True, blank=True)
    owner = models.ForeignKey(UserModel, null=True, blank=True, on_delete=models.CASCADE)
    owner_sessions = models.ManyToManyField(Session, db_table='article_owners', blank=True)
    content = models.TextField()
    date = models.DateField(default=date.today)

    def __str__(self): return str(self.slug)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(''.join(eval(settings.ALPHABET).get(w, w) for w in self.title.lower())) + \
                        self.date.strftime('-%m-%d')
        try:
            super(type(self), self).save(*args, **kwargs)
        except IntegrityError:
            articles = type(self).objects.all()
            exists_slug = [article.slug if self.slug in article.slug else None for article in articles]
            if len(exists_slug) != 1:
                number = [int(exist_slug.split('-')[-1]) for exist_slug in exists_slug][-1] + 1
                self.slug += f'-{number}'
            else:
                self.slug += '-2'

            super(type(self), self).save(*args, **kwargs)

    class Meta:
        db_table = 'articles'
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'


class Storage(models.Model):

    hash = models.CharField(max_length=255, unique=True, db_index=True, null=True, blank=True)
    use_hash = models.BooleanField(default=True)
    file = models.FileField(unique=True, db_index=True)
    date = models.DateField(default=date.today)

    def __str__(self): return str(self.file)

    def save(self, *args, **kwargs):
        salt = 'django.core.models.Storage'
        if self.use_hash:
            byte = self.file.read()

            self.hash = generate_data_hash(salt, byte, type(self))
            if type(self.hash) is bytes:
                return self.hash.decode()

            content_type = self.file.file.content_type.split('/')[-1]
            self.file.name = f'{self.hash[:32]}.{content_type}'

        super(type(self), self).save()

    class Meta:
        db_table = 'storage'
        verbose_name = 'Storage object'
        verbose_name_plural = 'Storage'