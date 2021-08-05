from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def try_login(request):
    username = request.POST['login']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse('ok')
    else:
        return HttpResponse('Incorrect data')

@csrf_exempt
def try_logout(request):
    if not getattr(request.user, 'is_authenticated', False):
        return HttpResponse('User is not authenticated', status=401)
    logout(request)
    return HttpResponse('ok')
