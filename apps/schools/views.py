from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from django_tenants.utils import remove_www

from .models import Domain
from .models import School
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


class SchoolListView(LoginRequiredMixin, ListView):
    context_object_name = 'schools'
    model = School
    # template_name = 'classrooms/classroom_list.html'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.annotate(students_amount=Count('students'))

    #     return queryset.order_by('name')

    # def get_queryset_classroom_parent(self):
    #     queryset = super().get_queryset_classroom_parent()
    #     queryset = queryset.annotate(students_amount=Count('students'))

    #     return queryset.order_by('name')

    # def get_queryset_classroom_student(self):
    #     queryset = super().get_queryset_classroom_student()
    #     queryset = queryset.annotate(students_amount=Count('students'))

    #     return queryset.order_by('name')

    # def get_context_data(self, *args, **kwargs):
    #     context = super(SchoolListView, self).get_context_data(*args, **kwargs)

    #     context[f'{self.context_object_name}_teacher'] = self.get_queryset_classroom_teacher()
    #     context[f'{self.context_object_name}_parent'] = self.get_queryset_classroom_parent()
    #     context[f'{self.context_object_name}_student'] = self.get_queryset_classroom_student()

    #     return context

    # def get_back_url(self):
    #     return None
