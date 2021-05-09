from .env import alphabet
from .forms import ArticleForm
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse('Hello, World!')

@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)

        if form.is_valid():
            article = form.save(commit=False)
            article.slug = slugify(''.join(alphabet.get(w, w) for w in article.title.lower()))
            article.author = request.user
            article.save()
            return HttpResponse('Hello, World!')
    else:
        form = ArticleForm()

    return render(request, 'create.html', {'form': form})