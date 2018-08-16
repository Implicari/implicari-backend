from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.urls import reverse

from classrooms.models import Classroom


User = get_user_model()


class ParentMixin:

    @cached_property
    def classroom(self):
        pk = self.kwargs.get('classroom_pk')
        return get_object_or_404(Classroom, pk=pk, creator=self.request.user)

    @cached_property
    def student(self):
        pk = self.kwargs.get('student_pk')
        return get_object_or_404(User, pk=pk, classrooms=self.classroom)

    def get_context_data(self, *args, **kwargs):
        context = super(ParentMixin, self).get_context_data(*args, **kwargs)

        context['classroom'] = self.classroom
        context['student'] = self.student

        return context

    def get_queryset(self):
        return self.get_queryset_parents()

    def get_queryset_parents(self):
        return self.model.objects.filter(students=self.student)


class ParentListView(LoginRequiredMixin, ParentMixin, ListView):
    context_object_name = 'parents'
    model = User
    template_name = 'parents/parent_list.html'


class ParentCreateView(LoginRequiredMixin, ParentMixin, CreateView):
    context_object_name = 'parent'
    fields = [
        'first_name',
        'last_name',
        'email',
        'avatar',
    ]
    model = User
    template_name = 'parents/parent_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        form.instance.students.add(self.student)

        return response

    def get_success_url(self):
        return reverse('student-detail', kwargs={
            'classroom_pk': self.classroom.id,
            'pk': self.student.id,
        })

    def get_context_data(self, *args, **kwargs):
        context = super(ParentCreateView, self).get_context_data(*args, **kwargs)

        context['back_url'] = reverse('student-detail', kwargs={
            'classroom_pk': self.classroom.id,
            'pk': self.student.id,
        })

        return context


class ParentDeleteView(LoginRequiredMixin, ParentMixin, DeleteView):
    context_object_name = 'parent'
    model = User
    template_name = 'parents/parent_confirm_delete.html'

    def get_success_url(self):
        return reverse('student-list', kwargs={
            'classroom_pk': self.classroom.id,
            'student_pk': self.student.id,
        })


class ParentDetailView(LoginRequiredMixin, ParentMixin, DetailView):
    context_object_name = 'parent'
    model = User
    template_name = 'parents/parent_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ParentDetailView, self).get_context_data(*args, **kwargs)

        context['back_url'] = reverse('student-detail', kwargs={
            'classroom_pk': self.classroom.id,
            'pk': self.student.id,
        })

        return context


class ParentUpdateView(LoginRequiredMixin, ParentMixin, UpdateView):
    context_object_name = 'parent'
    fields = [
        'first_name',
        'last_name',
        'avatar',
    ]
    model = User
    template_name = 'parents/parent_form.html'

    def get_success_url(self):
        return self.classroom.get_parent_list_url()

    def get_context_data(self, *args, **kwargs):
        context = super(ParentUpdateView, self).get_context_data(*args, **kwargs)

        context['back_url'] = reverse('parent-detail', kwargs={
            'classroom_pk': self.classroom.id,
            'student_pk': self.student.id,
            'pk': self.object.id,
        })

        return context
