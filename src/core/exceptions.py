from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render


@requires_csrf_token
def bad_request(request, exception):
    status = 400
    context = {
        'title': 'Bad Request',
        'status': status
    }
    return render(request, 'exception.html', context, status=status)


@requires_csrf_token
def permission_denied(request, exception):
    status = 403
    context = {
        'title': 'Forbidden',
        'status': status
    }
    return render(request, 'exception.html', context, status=status)


@requires_csrf_token
def page_not_found(request, exception):
    status = 404
    context = {
        'title': 'Page does not exist',
        'status': status
    }
    return render(request, 'exception.html', context, status=status)


@requires_csrf_token
def server_error(request):
    status = 500
    context = {
        'title': 'Internal Server Error',
        'status': status
    }
    return render(request, 'exception.html', context, status=status)
