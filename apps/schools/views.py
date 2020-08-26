from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

from django_tenants.utils import remove_www

from .models import Domain
from .forms import SigninForm


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'schools/index.html')


def signin(request: HttpRequest) -> HttpResponse:
    form = SigninForm(request.POST or None)

    if form.is_valid():
        subdomain = form.cleaned_data.get('subdomain')

        hostname_without_port = remove_www(request.get_host().split(':')[0])

        domain = Domain.objects.get(domain=f'{subdomain}.{hostname_without_port}')
        protocol = 'https' if request.is_secure() else 'http'

        return redirect(f'{protocol}://{domain.domain}:{request.get_port()}')

    return render(request, 'schools/signin.html', {'form': form})
