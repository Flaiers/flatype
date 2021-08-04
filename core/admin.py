from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'author', 'text', 'date',)
    list_display = ('title', 'slug', 'author', 'date',)
    autocomplete_fields = ('author',)
    search_fields = ('title', 'text',)
    date_hierarchy = 'date'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('author',)
        return self.readonly_fields
