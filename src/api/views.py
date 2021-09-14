from core.models import Article, Storage
from core.forms import ArticleForm, StorageForm

from django.contrib.sessions.models import Session

from django.middleware.csrf import get_token

from django.views.decorators.http import require_http_methods
from django.http import JsonResponse


@require_http_methods(["POST"])
def try_save(request):
    form = ArticleForm(request.POST)
    if not form.is_valid():
        return JsonResponse(
            {
                'error': True,
                'data': form.errors
            },
        )

    slug = form.data.get('page_id',)
    if slug != '0':
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            return JsonResponse(
                {
                    'error': True,
                    'data': 'Article not found'
                },
            )

        session_key = request.session.session_key

        if not (request.user == article.owner or \
               (session_key == str(article.owner_session) and \
               (session_key and article.owner_session) != None)):
            return JsonResponse(
                {
                    'error': True,
                    'data': 'Forbidden'
                },
            )

        article.title = form.cleaned_data.get('title',)
        article.author = form.cleaned_data.get('author',)
        article.text = form.cleaned_data.get('text',)

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

            session = Session.objects.get(pk=request.session.session_key)
            article.owner_session = session

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
                'data': form.errors
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
