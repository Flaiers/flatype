from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'date')
    search_fields = ('title', 'text')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date'
