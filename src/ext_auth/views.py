from core.models import Article

from django.contrib.auth.forms import AuthenticationForm

from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse


def try_check(request) -> JsonResponse:
    page_id = request.POST.get('page_id',)

    if page_id == '0':
        return JsonResponse({
            'short_name': f'👤 {request.user}',
            'author_name': str(request.user),
            'author_url': '#' if request.user.is_authenticated else '',
            'save_hash': '',
            'can_edit': False,
        })

    try:
        article = Article.objects.get(slug=page_id)
    except Article.DoesNotExist:
        return JsonResponse(
            {
                'error': True,
                'data': 'Article not found'
            },
            status=404
        )

    owner_hash = request.session.get('externalid',)

    return JsonResponse({
        'short_name': f'👤 {request.user}',
        'author_name': str(request.user),
        'author_url': '#' if request.user.is_authenticated else '',
        'save_hash': page_id,
        'can_edit': True if request.user == article.owner or \
                            owner_hash == article.owner_hash else False,
    })


@csrf_exempt
@require_http_methods(["POST"])
def try_login(request) -> JsonResponse:
    form = AuthenticationForm(data=request.POST)
    if not form.is_valid():
        return JsonResponse(
            {
                'error': True,
                'data': 'Form data is not valid'
            },
            status=422
        )

    if request.user.is_authenticated:
        return JsonResponse(
            {
                'error': True,
                'data': 'User already authenticated'
            },
            status=409
        )

    username = request.POST.get('username',)
    password = request.POST.get('password',)

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse(
            {
                'error': True,
                'data': 'User not found'
            },
            status=404
        )

    if not user.is_active:
        return JsonResponse(
            {
                'error': True,
                'data': 'User is locked'
            },
            status=423
        )

    login(request, user)
    return JsonResponse({
        'data': 'ok'
    })


def try_logout(request) -> JsonResponse:
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                'error': True,
                'data': 'User is not authenticated'
            },
            status=401
        )

    logout(request)
    return JsonResponse({
        'data': 'ok'
    })
