from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'author', 'owner', 'owner_hash', 'text', 'date',)
    list_display = ('title', 'slug', 'author', 'date',)
    search_fields = ('title', 'text',)
    date_hierarchy = 'date'

    def get_readonly_fields(self, request, obj=None) -> tuple:
        if obj:
            return self.readonly_fields + ('slug', 'owner', 'date',)
        return self.readonly_fields
