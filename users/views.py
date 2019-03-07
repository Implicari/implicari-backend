from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import UpdateView

from classrooms.models import Classroom

from .forms import UserCreationForm


User = get_user_model()


def signup(request):
    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        form.save()

        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')

        user = authenticate(email=email, password=raw_password)

        login(request, user)

        return redirect('classroom-create')

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

    def get_success_url(self):
        classrooms = Classroom.objects.distinct().filter(
            Q(creator=self.request.user) |
            Q(students__parents=self.request.user) |
            Q(students=self.request.user)
        )

        if not classrooms.exists():
            url = reverse('classroom-create')

        elif classrooms.count() == 1:
            url = classrooms.get().get_detail_url()

        else:
            url = reverse('classroom-list')

        return url
