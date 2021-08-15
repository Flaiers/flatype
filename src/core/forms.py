from django import forms

from .models import Article, Storage


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'author', 'text',)


class StorageForm(forms.ModelForm):

    class Meta:
        model = Storage
        fields = ('file',)
