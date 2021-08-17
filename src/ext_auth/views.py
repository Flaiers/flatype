from django.contrib.auth.forms import AuthenticationForm

from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse


@csrf_exempt
def try_check(request) -> JsonResponse:

    return JsonResponse({
        'author_name': str(request.user),
        'author_url': '#' if request.user.is_authenticated else '',
        'can_edit': False,
        'save_hash': '',
        'short_name': f'👤 {request.user}'
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

    username = request.POST.get('username')
    password = request.POST.get('password')

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


@csrf_exempt
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
