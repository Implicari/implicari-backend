from django.shortcuts import render
from django.shortcuts import redirect

from .models import Domain
from .forms import SignupForm


def index(request):
    return render(request, 'schools/index.html')


def signup(request):
    form = SignupForm(request.POST or None)

    if form.is_valid():
        form.save()

        subdomain = form.cleaned_data.get('subdomain')
        domain = Domain.objects.get(domain=subdomain)

        return redirect(domain.domain)

    return render(request, 'users/signup.html', {'form': form})
