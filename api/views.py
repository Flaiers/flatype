from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from core.models import Article
from core.forms import ArticleForm

from ext_auth.models import ExternalHashId

from packs.hashing import GenerateHash

from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.db.utils import IntegrityError


@csrf_exempt
@require_http_methods(["POST"])
def try_register(request):
    form = UserCreationForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'error': True, 'data': 'Form data is not valid'}, status=422)

    user = form.save(commit=False)
    user.first_name = request.POST.get('first_name', '')
    user.last_name = request.POST.get('last_name', '')
    user.email = request.POST.get('email', '')
    user.save()

    if owner_hash := request.session.get('externalid'):
        ExternalHashId.objects.create(user=user, session=owner_hash)


    return JsonResponse({'data': 'ok'})


@csrf_exempt
@require_http_methods(["POST"])
def try_login(request):
    form = AuthenticationForm(data=request.POST)
    if not form.is_valid():
        return JsonResponse({'error': True, 'data': 'Form data is not valid'})

    if request.user.is_authenticated:
        return JsonResponse({'error': True, 'data': 'User already authenticated'}, status=409)

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return JsonResponse({'data': 'ok'})
        else:
            return JsonResponse({'error': True, 'data': 'User is locked'}, status=423)
    else:
        return JsonResponse({'error': True, 'data': 'User not found'}, status=404)

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
        if owner_hash := request.session.get('externalid'):
            article.owner_hash = owner_hash
        else:
            article.owner_hash = GenerateHash(Article)
            request.session['externalid'] = article.owner_hash

    # TODO: переместить в модели
    try:
        article.save()
    except IntegrityError:
        exists_slug = []
        objects = Article.objects.all()
        [exists_slug.append(object.slug) if article.slug in object.slug else None for object in objects]
        print(exists_slug)
        if len(exists_slug) != 1:
            number = [int(exist_slug.split('-')[-1]) for exist_slug in exists_slug][-1] + 1
            article.slug += f'-{number}'
        else:
            article.slug += '-2'
        article.save()

    if external:
        return JsonResponse({'data': f"http://{request.headers['Host']}/{article.slug}"})

    return article

# TODO: Валидация по форме
@csrf_exempt
@require_http_methods(["POST"])
def try_edit(request, article=None, external=False):
    if article is None:
        try:
            article = Article.objects.get(slug=request.POST.get('article'))
            external = True
        except:
            return JsonResponse({'error': True, 'data': 'Article not found'}, status=404)

    if external:

        owner_hash = request.session.get('externalid')
        if not owner_hash:

            session_key = request.session.session_key
            object = Session.objects.get(session_key=session_key)
            user_id = int(object.get_decoded()['_auth_user_id'])
            request.user = User.objects.get(id=user_id)

        if not (request.user == article.owner or article.owner_hash == owner_hash):
            return JsonResponse({'error': True, 'data': 'User is not authenticated'}, status=401)

    article.title = request.POST.get('title')

    if request.POST.get('author'):
        article.author = request.POST.get('author')

    article.text = request.POST.get('text')
    article.save()

    if external:
        return JsonResponse({'data': 'ok'})

    return article
