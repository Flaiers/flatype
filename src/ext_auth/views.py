from core.models import Article
from .forms import UserCreationForm

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
            'author_url': request.user.link if request.user.is_authenticated else '',
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

    session_key = request.session.session_key

    return JsonResponse({
        'short_name': f'👤 {request.user}',
        'author_name': str(request.user),
        'author_url': request.user.link if request.user.is_authenticated else '',
        'can_edit': True if request.user == article.owner or \
                           (session_key == str(article.owner_session) and \
                           (session_key and article.owner_session) != None) \
                            else False,
    })


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

    login(request, user)
    return JsonResponse({
        'data': 'ok'
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
