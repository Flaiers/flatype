from .models import Article

from django.shortcuts import get_object_or_404

from django.utils.html import format_html
from django.views.generic import TemplateView
from django.shortcuts import render


class Create(TemplateView):
    template_name = 'create.html'


class View(TemplateView):

    def get(self, request, slug: str, *args, **kwargs):
        article = get_object_or_404(Article, slug=slug)

        return render(
            request,
            'view.html',
            {
                'article': article,
                'content': format_html(article.text),
                'date': article.date.strftime('%B %d, %Y'),
            }
        )
