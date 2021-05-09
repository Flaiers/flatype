from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify

class Article(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        #return slugify(self.title)
        return self.title