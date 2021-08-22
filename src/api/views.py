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
                'data': 'Form data is not valid'
            },
            status=422
        )

    user = form.save(commit=False)
    user.first_name = request.POST.get('first_name', '')
    user.last_name = request.POST.get('last_name', '')
    user.email = request.POST.get('email', '')
    user.save()

    if owner_hash := request.session.get('externalid'):
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
                'data': 'Form data is not valid'
            },
            status=422
        )
    
    slug = request.POST.get('save_hash')
    if slug != '':
        owner_hash = request.session.get('externalid')

        try:
            article = Article.objects.get(slug=slug)

            if not (request.user == article.owner or owner_hash == article.owner_hash):
                return JsonResponse(
                    {
                        'error': True,
                        'data': 'Forbidden'
                    },
                    status=403
                )

        except Exception:
            return JsonResponse(
                {
                    'error': True,
                    'data': 'Article not found'
                },
                status=404
            )

        article.title = request.POST.get('title')

        if request.POST.get('author'):
            article.author = request.POST.get('author')

        if request.user.is_authenticated and owner_hash and article.owner is None:
            article.owner = request.user

        article.text = request.POST.get('text')
        article.save()

    else:
        article = form.save(commit=False)

        if article.author is None:
            article.author = request.user

        if request.user.is_authenticated:
            article.owner = request.user
        else:
            if owner_hash := request.session.get('externalid'):
                article.owner_hash = owner_hash
            else:
                article.owner_hash = GenerateRandomHash(Article)
                request.session['externalid'] = article.owner_hash

        article.save()

    return JsonResponse({
        'path': article.slug
    })


@require_http_methods(["POST"])
def try_upload(request) -> JsonResponse:
    form = StorageForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse(
            {
                'error': True,
                'data': 'Form data is not valid'
            },
            status=422
        )

    file = request.FILES.get('file')
    instance = Storage(file=file)
    object = instance.save(type=file.content_type.split('/')[-1], bytes=file.read())

    object = instance if object is None else object

    return JsonResponse(
        [
            {
                'src': f'/media/{object}'
            }
        ],
        safe=False
    )
