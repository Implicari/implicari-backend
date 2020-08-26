from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse


def index(request: HttpRequest) -> HttpResponse:
    response: HttpResponse

    if request.user.is_authenticated:
        response = redirect(reverse('classroom-list'))

    else:
        response = render(request, 'index.html')

    return response
