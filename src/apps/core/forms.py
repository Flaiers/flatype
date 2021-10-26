from .models import Article, Storage

from django import forms


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'author', 'content',)


class StorageForm(forms.ModelForm):

    class Meta:
        model = Storage
        fields = ('file',)
