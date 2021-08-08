from datetime import date
from django.conf import settings
from django.utils.text import slugify

from django.db import models
from django.contrib.auth.models import User

from django.db.utils import IntegrityError


class Article(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, db_index=True)
    author = models.CharField(max_length=64, null=True, blank=True)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    owner_hash = models.CharField(max_length=32, null=True, blank=True)
    text = models.TextField()
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(''.join(eval(settings.ALPHABET).get(w, w) for w in self.title.lower())) + self.date.strftime('-%m-%d')
        try:
            super(Article, self).save(*args, **kwargs)
        except IntegrityError:
            exists_slug = []
            objects = Article.objects.all()
            [exists_slug.append(object.slug) if self.slug in object.slug else None for object in objects]
            if len(exists_slug) != 1:
                number = [int(exist_slug.split('-')[-1]) for exist_slug in exists_slug][-1] + 1
                self.slug += f'-{number}'
            else:
                self.slug += '-2'

            super(Article, self).save(*args, **kwargs)
