from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

from .models import Domain
from .forms import SigninForm


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'schools/index.html')


def signin(request: HttpRequest) -> HttpResponse:
    form = SigninForm(request.POST or None)

    if form.is_valid():
        # form.save()

        subdomain = form.cleaned_data.get('subdomain')
        domain = Domain.objects.get(domain=subdomain)

        return redirect(domain.domain)

    return render(request, 'schools/signin.html', {'form': form})
