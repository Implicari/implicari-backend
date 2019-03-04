from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView


User = get_user_model()


def signup(request):
    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        form.save()

        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')

        user = authenticate(username=username, password=raw_password)

        login(request, user)

        return redirect('index')

    return render(request, 'users/signup.html', {'form': form})


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    context_object_name = 'user'
    model = User
    fields = [
        'email',
        'first_name',
        'last_name',
    ]
    template_name = 'users/user_form.html'

    def get_object(self):
        return self.request.user


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    fields = [
        'avatar',
        'email',
        'first_name',
        'last_name',
    ]

    def get_success_url(self):
        return self.object.get_detail_url()


class UserDetailView(DetailView):
    model = User


class UserUpdateView(LoginRequiredMixin, UpdateView):
    context_object_name = 'user'
    model = User
    fields = [
        'avatar',
        'first_name',
        'last_name',
    ]
