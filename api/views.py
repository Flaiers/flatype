from core.models import Article
from core.forms import ArticleForm
from packs.hashing import GenerateHash

from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.db.utils import IntegrityError


@csrf_exempt
@require_http_methods(["POST"])
def try_login(request):
    if request.user.is_authenticated:
        return JsonResponse({'error': True, 'data': 'User already authenticated'}, status=409)

    username = request.POST['login']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return JsonResponse({'data': 'ok'})
        else:
            return JsonResponse({'error': True, 'data': 'User is locked'}, status=423)
    else:
        return JsonResponse({'error': True, 'data': 'User not found'}, satus=404)

@csrf_exempt
@require_http_methods(["POST"])
def try_logout(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': True, 'data': 'User is not authenticated'}, status=401)

    logout(request)
    return JsonResponse({'data': 'ok'})

@csrf_exempt
@require_http_methods(["POST"])
def try_save(request, form=None, external=False):
    if form is None:
        form = ArticleForm(request.POST)
        external = True

        if not form.is_valid():
            return JsonResponse({'error': True, 'data': 'Form data is not valid'}, status=422)

    article = form.save(commit=False)

    if article.author is None:
        article.author = request.user

    if request.user.is_authenticated:
        article.owner = request.user
    else:
        owner_hash = request.COOKIES.get('owner_hash')
        if owner_hash:
            article.owner_hash = owner_hash
        else:
            article.owner_hash = GenerateHash(Article)

    try:
        article.save()
    except IntegrityError:
        objects = Article.objects.filter(title=article.title)
        if len(objects) != 1:
            number = [int(object.slug.split('-')[-1]) for object in objects][-1]
            article.slug += f'-{number + 1}'
        else:
            article.slug += '-2'
        article.save()

    if external:
        return JsonResponse({'data': f"http://{request.headers['Host']}/{article.slug}"})

    return article

@csrf_exempt
@require_http_methods(["POST"])
def try_edit(request, article=None, external=False):
    if article is None:
        try:
            article = Article.objects.get(slug=request.POST.get('article', None))
            external = True
        except:
            return JsonResponse({'error': True, 'data': 'Article not found'}, satus=404)

    article.title = request.POST.get('title')

    if request.POST.get('author'):
        article.author = request.POST.get('author')

    article.text = request.POST.get('text')
    article.save()

    if external:
        return JsonResponse({'data': 'ok'})

    return article
