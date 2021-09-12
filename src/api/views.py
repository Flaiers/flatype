from django.contrib.auth.forms import UserCreationForm

from core.models import Article, Storage
from core.forms import ArticleForm, StorageForm

from ext_auth.models import ExternalHashId

from packs.hashing import GenerateRandomHash

from django.views.decorators.http import require_http_methods
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
@require_http_methods(["POST"])
def try_register(request) -> JsonResponse:
    form = UserCreationForm(request.POST)
    if not form.is_valid():
        return JsonResponse(
            {
                'error': True,
                'data': 'Data is not valid'
            },
        )

    user = form.save(commit=False)
    user.first_name = form.data.get('first_name', '')
    user.last_name = form.data.get('last_name', '')
    user.email = form.data.get('email', '')
    user.save()

    if owner_hash := request.session.get('_ext_auth_hash',):
        ExternalHashId.objects.create(user=user, session=owner_hash)

        articles = Article.objects.filter(owner_hash=owner_hash)
        for article in articles:
            article.owner = user
            article.save()

    login(request, user)
    return JsonResponse({
        'data': 'ok'
    })


@require_http_methods(["POST"])
def try_save(request):
    form = ArticleForm(request.POST)
    if not form.is_valid():
        return JsonResponse(
            {
                'error': True,
                'data': 'Data is not valid'
            },
        )

    slug = form.data.get('save_hash',)
    if slug != '':
        owner_hash = request.session.get('_ext_auth_hash',)

        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            return JsonResponse(
                {
                    'error': True,
                    'data': 'Article not found'
                },
            )

        if not (request.user == article.owner or \
               (owner_hash == article.owner_hash and \
               (owner_hash and article.owner_hash) != None)):
            return JsonResponse(
                {
                    'error': True,
                    'data': 'Forbidden'
                },
            )

        article.title = form.cleaned_data.get('title',)
        article.author = form.cleaned_data.get('author',)
        article.text = form.cleaned_data.get('text',)

        if request.user.is_authenticated and owner_hash and article.owner is None:
            article.owner = request.user

        article.save()

    else:
        article = form.save(commit=False)

        if request.user.is_authenticated:
            article.owner = request.user
        else:
            if owner_hash := request.session.get('_ext_auth_hash',):
                article.owner_hash = owner_hash
            else:
                article.owner_hash = GenerateRandomHash(Article)
                request.session['_ext_auth_hash'] = article.owner_hash

        article.save()

    return JsonResponse({
        'page_id': article.slug,
        'path': article.slug
    })


@require_http_methods(["POST"])
def try_upload(request) -> JsonResponse:
    form = StorageForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse(
            {
                'error': True,
                'data': 'Data is not valid'
            },
        )

    file = request.FILES.get('file',)
    instance = Storage(file=file)
    object = instance.save(type=file.content_type.split('/')[-1], bytes=file.read())

    return JsonResponse(
        [
            {
                'src': f'/media/{instance if object is None else object}'
            }
        ],
        safe=False
    )
