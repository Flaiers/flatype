from api.views import try_edit

from .models import Article
from .forms import ArticleForm

from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views.decorators.csrf import requires_csrf_token


class Create(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'create.html'
        )


class View(TemplateView):

    def get(self, request, slug: str, *args, **kwargs):
        try:
            article = Article.objects.get(slug=slug)
        except Exception:
            return render(
                request,
                'exceptions/404.html',
                status=404
            )

        owner_hash = request.session.get('externalid')
        if request.GET.get('edit', False) and \
            (request.user == article.owner or owner_hash == article.owner_hash):

            form = ArticleForm(instance=article)

            return render(request, 'write.html', {'form': form})

        return render(
            request,
            'view.html',
            {
                'article': article,
                'owner_hash': owner_hash,
                'date': article.date.strftime('%B %d, %Y'),
            }
        )

    def post(self, request, slug: str, *args, **kwargs):
        try:
            article = Article.objects.get(slug=slug)
        except Exception:
            return render(
                request,
                'exceptions/404.html',
                status=404
            )

        owner_hash = request.session.get('externalid')
        if request.GET.get('edit', False) and \
            (request.user == article.owner or owner_hash == article.owner_hash):

            form = ArticleForm(request.POST)
            if form.is_valid():
                article = try_edit(request, article)

                return redirect('view', slug=article.slug)


class Exceptions:

    @requires_csrf_token
    def bad_request(self, request, exception):
        return render(request, 'exceptions/400.html', status=400)

    @requires_csrf_token
    def permission_denied(self, request, exception):
        return render(request, 'exceptions/403.html', status=403)

    @requires_csrf_token
    def page_not_found(self, request, exception):
        return render(request, 'exceptions/404.html', status=404)

    @requires_csrf_token
    def server_error(self, request):
        return render(request, 'exceptions/500.html', status=500)
