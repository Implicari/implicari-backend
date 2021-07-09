from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


def index(request: HttpRequest) -> HttpResponse:
    viewname = 'classroom-list' if request.user.is_authenticated else 'login'
    url = reverse(viewname)
    response = redirect(url)

    return response
