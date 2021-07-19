from datetime import date
from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name="Tittle")
    slug = models.SlugField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Your story")
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.slug
