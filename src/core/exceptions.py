from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render


@requires_csrf_token
def bad_request(request, exception):
    return render(request, 'exceptions/400.html', status=400)


@requires_csrf_token
def permission_denied(request, exception):
    return render(request, 'exceptions/403.html', status=403)


@requires_csrf_token
def page_not_found(request, exception):
    return render(request, 'exceptions/404.html', status=404)


@requires_csrf_token
def server_error(request):
    return render(request, 'exceptions/500.html', status=500)
