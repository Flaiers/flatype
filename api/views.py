from core.models import Article

from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from django.db.utils import IntegrityError
from django.contrib.auth.models import User


@csrf_exempt
@require_http_methods(["POST"])
def try_login(request):
    username = request.POST['login']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse('ok')
        else:
            return HttpResponse('Disabled account')
    else:
        return HttpResponse('Incorrect data')

@csrf_exempt
def try_logout(request):
    if not getattr(request.user, 'is_authenticated', False):
        return HttpResponse('User is not authenticated', status=401)
    logout(request)
    return HttpResponse('ok')


def create(request, form):
    article = form.save(commit=False)

    if article.author is None:
        article.author = request.user

    if request.user.is_authenticated:
        article.owner = request.user

    try:
        article.save()
    except IntegrityError:
        objects = Article.objects.filter(title=article.title)
        number = [int(object.slug.split('-')[-1]) for object in objects][-1]
        article.slug += f'-{number + 1}'
        article.save()

    return article

def edit(request, article):
    article.title = request.POST.get('title')
    article.text = request.POST.get('text')
    article.save()

    return article
