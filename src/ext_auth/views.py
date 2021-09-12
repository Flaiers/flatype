from core.models import Article

from django.contrib.auth.forms import AuthenticationForm

from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse


def try_check(request) -> JsonResponse:
    slug = request.POST.get('page_id',)

    if slug == '0':
        return JsonResponse({
            'short_name': f'👤 {request.user}',
            'author_name': str(request.user),
            'author_url': '#' if request.user.is_authenticated else '',
            'save_hash': '',
            'can_edit': False,
        })

    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        return JsonResponse(
            {
                'error': True,
                'data': 'Article not found'
            },
        )

    owner_hash = request.session.get('_ext_auth_hash',)

    return JsonResponse({
        'short_name': f'👤 {request.user}',
        'author_name': str(request.user),
        'author_url': request.user.link if request.user.is_authenticated else '',
        'save_hash': slug,
        'can_edit': True if request.user == article.owner or \
                           (owner_hash == article.owner_hash and \
                           (owner_hash and article.owner_hash) != None) \
                            else False,
    })


@csrf_exempt
@require_http_methods(["POST"])
def try_login(request) -> JsonResponse:
    form = AuthenticationForm(data=request.POST)
    if not form.is_valid():
        return JsonResponse(
            {
                'error': True,
                'data': 'Data is not valid'
            },
        )

    if request.user.is_authenticated:
        return JsonResponse(
            {
                'error': True,
                'data': 'User already authenticated'
            },
        )

    username = form.cleaned_data.get('username',)
    password = form.cleaned_data.get('password',)

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse(
            {
                'error': True,
                'data': 'User not found'
            },
        )

    if not user.is_active:
        return JsonResponse(
            {
                'error': True,
                'data': 'User is locked'
            },
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
        )

    logout(request)
    return JsonResponse({
        'data': 'ok'
    })
