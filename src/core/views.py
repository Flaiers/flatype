from .models import Article

from .exceptions import page_not_found

from django.utils.html import format_html
from django.views.generic import TemplateView
from django.shortcuts import render


class Create(TemplateView):
    template_name = 'create.html'


class View(TemplateView):

    def get(self, request, slug: str, *args, **kwargs):
        try:
            article = Article.objects.get(slug=slug)
        except Exception as e:
            return page_not_found(request, e)

        return render(request, 'view.html',
            {
                'article': article,
                'content': format_html(article.text),
                'date': article.date.strftime('%B %d, %Y'),
            }
        )
