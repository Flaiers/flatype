from core.models import Article, Storage
from core.forms import ArticleForm, StorageForm

from django.contrib.sessions.models import Session

from django.middleware.csrf import get_token

from django.views.decorators.http import require_http_methods
from django.http import JsonResponse


@require_http_methods(["POST"])
def try_save(request) -> JsonResponse:
    form = ArticleForm(request.POST)
    if not form.is_valid():
        return JsonResponse({
            'error': True,
            'data': form.errors
        })

    slug = form.data.get('page_id',)
    if slug != '0':
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            return JsonResponse({
                'error': True,
                'data': 'Article not found'
            })

        session_key = request.session.session_key
        owner_session = [str(session) for session in article.owner_session.all()]

        if not (request.user == article.owner or
                (session_key in owner_session and
                 session_key is not None)):
            return JsonResponse(
                {
                    'error': True,
                    'data': 'Forbidden'
                },
                status=403
            )

        article.title = form.cleaned_data.get('title',)
        article.author = form.cleaned_data.get('author',)
        article.content = form.cleaned_data.get('content',)

        if request.user.is_authenticated and session_key and article.owner is None:
            article.owner = request.user

        article.save()

    else:
        article = form.save(commit=False)

        if request.user.is_authenticated:
            article.owner = request.user
        else:
            if request.session.session_key is None:
                request.session['_csrftoken'] = get_token(request)

            article.save()
            article.owner_session.add(request.session.session_key)

        article.save()

    return JsonResponse({
        'page_id': article.slug,
        'path': article.slug
    })


@require_http_methods(["POST"])
def try_upload(request) -> JsonResponse:
    form = StorageForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse({
            'error': True,
            'data': form.errors
        })

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
