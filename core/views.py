from .models import Article
from .forms import ArticleForm

from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import requires_csrf_token


@login_required
def create_new(request):
    if request.method == 'POST':

        form = ArticleForm(request.POST)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()

            return redirect('article', slug=article.slug)
    else:
        form = ArticleForm()

    return render(request, 'create_new.html', {'form': form})


@login_required
def viewing(request, slug):
    article = Article.objects.get(slug=slug)
    return render(request, 'article.html', {
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
