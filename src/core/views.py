from .models import Article

from django.shortcuts import get_object_or_404

from django.utils.html import format_html
from django.views.generic import TemplateView, DetailView
from django.shortcuts import render


class Create(TemplateView):

    template_name = 'create.html'


class View(DetailView):

    model = Article
    queryset = Article.objects.all()
    template_name = 'view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        article = context['article']
        context['title'] = article.title
        context['author'] = article.author if article.author is not None else ''
        context['date'] = article.date.strftime('%B %d, %Y')
        context['content'] = format_html(article.content)
        return context
