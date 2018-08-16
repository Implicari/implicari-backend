from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from .models import Classroom


class ClassroomMixin:

    def get_queryset(self):
        return self.get_queryset_classroom()

    def get_queryset_classroom(self):
        return self.model.objects.filter(creator=self.request.user)


class ClassroomListView(LoginRequiredMixin, ClassroomMixin, ListView):
    context_object_name = 'classrooms'
    model = Classroom

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(students_amount=Count('students'))

        return queryset.order_by('name')


class ClassroomCreateView(LoginRequiredMixin, ClassroomMixin, CreateView):
    model = Classroom
    fields = [
        'name',
        'is_archived',
        'students',
    ]

    def form_valid(self, form):
        form.instance.creator = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_list_url()


class ClassroomDeleteView(LoginRequiredMixin, ClassroomMixin, DeleteView):
    model = Classroom

    def get_success_url(self):
        return self.object.get_list_url()


class ClassroomDetailView(LoginRequiredMixin, ClassroomMixin, DetailView):
    model = Classroom

    def get_context_data(self, *args, **kwargs):
        context = super(ClassroomDetailView, self).get_context_data(*args, **kwargs)

        context['back_url'] = reverse('classroom-list')

        return context


class ClassroomUpdateView(LoginRequiredMixin, ClassroomMixin, UpdateView):
    fields = [
        'name',
        'is_archived',
    ]
    model = Classroom

    def get_success_url(self):
        return self.object.get_list_url()

    def get_context_data(self, *args, **kwargs):
        context = super(ClassroomUpdateView, self).get_context_data(*args, **kwargs)

        context['back_url'] = reverse('classroom-detail', kwargs={'pk': self.object.id})

        return context
