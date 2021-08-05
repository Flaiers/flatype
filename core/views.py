from api.views import create, edit

from .models import Article
from .forms import ArticleForm

from django.shortcuts import render, redirect
from django.views.decorators.csrf import requires_csrf_token


def create_new(request):
    if request.method == 'POST':

        form = ArticleForm(request.POST)

        if form.is_valid():
            article = create(request, form)

            return redirect('viewing', slug=article.slug)
    else:
        form = ArticleForm()

    return render(request, 'create_new.html', {'form': form})


def viewing(request, slug):
    try:
        article = Article.objects.get(slug=slug)
    except:
        return render(request, 'exceptions/404.html', status=404)

    if request.GET.get('edit', False) and request.user == article.author:

        if request.method == 'POST':

            form = ArticleForm(request.POST)
            if form.is_valid():
                article = edit(request, article)

                return redirect('viewing', slug=article.slug)

        else:
            form = ArticleForm(instance=article)

            return render(request, 'writing.html', {'form': form})

    return render(request, 'viewing.html', {
        'title': article.title,
        'author': article.author,
        'date': article.date.strftime('%B %d, %Y'),
        'text': article.text
    })


class Exceptions():

    def __init__(self):
        return

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
