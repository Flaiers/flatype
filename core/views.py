from .models import Article
from .forms import ArticleForm

from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
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

        form = ArticleForm(request.POST)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user

            try:
                article.save()
            except IntegrityError:
                objects = Article.objects.filter(title=article.title)
                number = [int(object.slug.split('-')[-1]) for object in objects][-1]
                article.slug += f'-{number + 1}'
                article.save()

            return redirect('viewing', slug=article.slug)
    else:
        form = ArticleForm()

    return render(request, 'create_new.html', {'form': form})


@login_required
def viewing(request, slug):
    article = Article.objects.get(slug=slug)

    if request.GET.get('edit', False) and request.user == article.author:

        if request.method == 'POST':

            form = ArticleForm(request.POST)
            if form.is_valid():
                article.title = request.POST.get('title')
                article.text = request.POST.get('text')
                article.save()

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
