from django.contrib import admin

from .models import Article, Storage


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'author', 'owner', 'owner_session', 'content', 'date',)
    list_display = ('title', 'slug', 'author', 'date',)
    search_fields = ('title', 'content',)
    date_hierarchy = 'date'

    def get_readonly_fields(self, request, obj=None) -> tuple:
        if obj:
            return self.readonly_fields + ('slug', 'owner', 'date',)
        return self.readonly_fields


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    fields = ('hash', 'file', 'date', 'use_hash',)
    list_display = ('file', 'hash', 'date',)
    list_display_links = ('date',)
    search_fields = ('file', 'hash', 'date',)
    date_hierarchy = 'date'

    def get_readonly_fields(self, request, obj=None) -> tuple:
        if obj:
            return self.readonly_fields + ('hash', 'file', 'date', 'use_hash',)
        return self.readonly_fields
