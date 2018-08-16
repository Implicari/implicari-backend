from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse


def index(request):
    if request.user.is_authenticated:
        response = redirect(reverse('classroom-list'))

    else:
        response = render(request, 'index.html')

    return response
