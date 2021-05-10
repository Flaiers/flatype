import environ
from datetime import date
from .forms import ArticleForm
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required


def page_404(request):
    return render(request, 'page_404.html')


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
            article.slug = slugify(''.join(eval(env('ALPHABET')).get(w, w) for w in article.title.lower())) + date.strftime('-%m-%d')
            article.author = request.user
            article.save()
            return HttpResponse('Hello, World!')
    else:
        form = ArticleForm()

    return render(request, 'create_new.html', {'form': form})