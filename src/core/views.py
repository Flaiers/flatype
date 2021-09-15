from .models import Article

from django.utils.html import format_html
from django.views.generic import TemplateView, DetailView


class Create(TemplateView):

    template_name = 'create.html'


class View(DetailView):

    model = Article
    queryset = Article.objects.all()
    template_name = 'view.html'

    def get_context_data(self, *args, **kwargs):
        article = super().get_context_data(*args, **kwargs)['article']
        context = {
            'title': article.title,
            'author': article.author if article.author is not None else '',
            'date': article.date,
            'content': format_html(article.content)
        }
        return context
