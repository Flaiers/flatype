from core.models import Article

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.db.utils import IntegrityError
from django.contrib.auth.models import User


@csrf_exempt
def try_login(request):
    username = request.POST['login']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse('ok')
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

    request.user = User.objects.get(username=request.user) if str(request.user) == 'AnonymousUser' else request.user
    article.author = request.user

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
