import environ
from .models import Article
from .forms import ArticleForm
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import requires_csrf_token


def test(request):
    article = Article.objects.get(slug=request.path_info.replace('/', ''))
    return render(request, 'test.html', {
                    'title': article.title,
                    'author': article.author,
                    'text': article.text
                })


@login_required
def create_new(request):
    if request.method == 'POST':
        env = environ.Env(
            DEBUG=(bool, True)
        )
        environ.Env.read_env('./.env')

        form = ArticleForm(request.POST)

        if form.is_valid():
            article = form.save(commit=False)
            date = article.date
            article.slug = slugify(''.join(eval(env('ALPHABET')).get(w, w) 
                for w in article.title.lower())) + date.strftime('-%m-%d')

            article.author = request.user
            article.save()
            return HttpResponse('Hello, World!')
    else:
        form = ArticleForm()

    return render(request, 'create_new.html', {'form': form})


@login_required
def viewing(request):
    article = Article.objects.get(slug=request.path_info.replace('/', ''))
    return render(request, 'article.html', {
                    'title': article.title,
                    'author': article.author,
                    'text': article.text
                })


class Exceptions():

    def __init__(self):
        return

    @requires_csrf_token
    def page_not_found(self, request, exception):
        return render(request, 'exceptions/404.html', status=404)

    @requires_csrf_token
    def server_error(self, request):
        return render(request, 'exceptions/500.html', status=500)

    @requires_csrf_token
    def bad_request(self, request, exception):
        return render(request, 'exceptions/400.html', status=400)

    @requires_csrf_token
    def permission_denied(self, request, exception):
        return render(request, 'exceptions/403.html', status=403)
