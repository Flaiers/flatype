from api.views import try_edit

from .models import Article
from .forms import ArticleForm

from .exceptions import page_not_found

from django.utils.html import format_html
from django.views.generic import TemplateView
from django.shortcuts import render, redirect


class Create(TemplateView):
    template_name = 'create.html'


class View(TemplateView):

    def get(self, request, slug: str, *args, **kwargs):
        try:
            article = Article.objects.get(slug=slug)
        except Exception as e:
            return page_not_found(request, e)

        owner_hash = request.session.get('externalid')
        if request.GET.get('edit', False) and \
            (request.user == article.owner or owner_hash == article.owner_hash):

            form = ArticleForm(instance=article)

            return render(request, 'write.html',
                {
                    'form': form
                }
            )

        return render(request, 'view.html',
            {
                'article': article,
                'owner_hash': owner_hash,
                'content': format_html(article.text),
                'date': article.date.strftime('%B %d, %Y'),
            }
        )

    def post(self, request, slug: str, *args, **kwargs):
        try:
            article = Article.objects.get(slug=slug)
        except Exception as e:
            return page_not_found(request, e)

        owner_hash = request.session.get('externalid')
        if request.GET.get('edit', False) and \
            (request.user == article.owner or owner_hash == article.owner_hash):

            form = ArticleForm(request.POST)
            if form.is_valid():
                article = try_edit(request, article)

                return redirect('view', slug=article.slug)
