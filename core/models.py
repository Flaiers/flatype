from datetime import date

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name="Tittle")
    slug = models.SlugField(unique=True, db_index=True)
    author = models.CharField(max_length=64, null=True, blank=True, verbose_name="Your name")
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    owner_hash = models.CharField(max_length=32, null=True, blank=True)
    text = models.TextField(verbose_name="Your story")
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(''.join(eval(settings.ALPHABET).get(w, w) for w in self.title.lower())) + self.date.strftime('-%m-%d')
        super(Article, self).save(*args, **kwargs)
