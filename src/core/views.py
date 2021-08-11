from api.views import try_save, try_edit

from .models import Article
from .forms import ArticleForm

from django.shortcuts import render, redirect
from django.views.decorators.csrf import requires_csrf_token


def create_new(request):
    if request.method == 'POST':

        form = ArticleForm(request.POST)

        if form.is_valid():
            article = try_save(request, form)

            return redirect('viewing', slug=article.slug)
    else:
        form = ArticleForm()

    return render(request, 'create_new.html', {'form': form})


def viewing(request, slug: str):
    try:
        article = Article.objects.get(slug=slug)
    except Exception:
        return render(request, 'exceptions/404.html', status=404)

    owner_hash = request.session.get('externalid')
    if request.GET.get('edit', False) and \
            (request.user == article.owner or owner_hash == article.owner_hash):

        if request.method == 'POST':

            form = ArticleForm(request.POST)
            if form.is_valid():
                article = try_edit(request, article)

                return redirect('viewing', slug=article.slug)

        else:
            form = ArticleForm(instance=article)

            return render(request, 'writing.html', {'form': form})

    return render(request, 'viewing.html', {
        'article': article,
        'owner_hash': owner_hash,
        'date': article.date.strftime('%B %d, %Y'),
    })


class Exceptions:

    def __init__(self):
        return

    @requires_csrf_token
    def bad_request(self, request, exception) -> render:
        return render(request, 'exceptions/400.html', status=400)

    @requires_csrf_token
    def permission_denied(self, request, exception) -> render:
        return render(request, 'exceptions/403.html', status=403)

    @requires_csrf_token
    def page_not_found(self, request, exception) -> render:
        return render(request, 'exceptions/404.html', status=404)

    @requires_csrf_token
    def server_error(self, request) -> render:
        return render(request, 'exceptions/500.html', status=500)
