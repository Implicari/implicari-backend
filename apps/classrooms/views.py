from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView

from .models import Classroom


class ClassroomMixin:

    def get_queryset_classroom_teacher(self):
        return self.model.objects.filter(creator=self.request.user)

    def get_queryset_classroom_parent(self):
        return self.model.objects.filter(students__parents__in=self.request.user.persons.all())

    def get_queryset_classroom_student(self):
        return self.model.objects.filter(students__in=self.request.user.persons.all())

    def get_context_data(self, *args, **kwargs):
        context = super(ClassroomMixin, self).get_context_data(*args, **kwargs)

        context['back_url'] = self.get_back_url()

        return context

    def get_back_url(self):
        raise NotImplementedError


class ClassroomListView(LoginRequiredMixin, ClassroomMixin, TemplateView):
    context_object_name = 'classrooms'
    model = Classroom
    template_name = 'classrooms/classroom_list.html'

    def get_queryset_classroom_teacher(self):
        queryset = super().get_queryset_classroom_teacher()
        queryset = queryset.annotate(students_amount=Count('students'))

        return queryset.order_by('name')

    def get_queryset_classroom_parent(self):
        queryset = super().get_queryset_classroom_parent()
        queryset = queryset.annotate(students_amount=Count('students'))

        return queryset.order_by('name')

    def get_queryset_classroom_student(self):
        queryset = super().get_queryset_classroom_student()
        queryset = queryset.annotate(students_amount=Count('students'))

        return queryset.order_by('name')

    def get_context_data(self, *args, **kwargs):
        context = super(ClassroomListView, self).get_context_data(*args, **kwargs)

        context[f'{self.context_object_name}_teacher'] = self.get_queryset_classroom_teacher()
        context[f'{self.context_object_name}_parent'] = self.get_queryset_classroom_parent()
        context[f'{self.context_object_name}_student'] = self.get_queryset_classroom_student()

        return context

    def get_back_url(self):
        return None


class ClassroomCreateView(LoginRequiredMixin, ClassroomMixin, CreateView):
    model = Classroom
    fields = [
        'name',
    ]

    def form_valid(self, form):
        form.instance.creator = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_list_url()

    def get_back_url(self):
        return reverse('classroom-list')


class ClassroomDeleteView(LoginRequiredMixin, ClassroomMixin, DeleteView):
    model = Classroom

    def get_queryset(self):
        return self.model.objects.filter(creator=self.request.user)

    def get_success_url(self):
        return self.object.get_list_url()

    def get_back_url(self):
        return self.object.get_detail_url()


class ClassroomDetailView(LoginRequiredMixin, ClassroomMixin, DetailView):
    model = Classroom

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        classroom = self.get_object()

        if not (
            classroom.creator_id == user.id or
            classroom.students.filter(id=user.id).exists() or
            classroom.students.filter(parents=user).exists()
        ):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ClassroomDetailView, self).get_context_data(*args, **kwargs)

        context['students'] = self.get_students()

        return context

    def get_back_url(self):
        return reverse('classroom-list')

    def get_students(self):
        user = self.request.user
        classroom = self.get_object()

        if classroom.creator_id == user.id:
            students = classroom.students.all()

        elif classroom.students.filter(id=user.id).exists():
            students = classroom.students.filter(id=user.id)

        elif classroom.students.filter(parents=user).exists():
            students = classroom.students.filter(parents=user)

        return students


class ClassroomUpdateView(LoginRequiredMixin, ClassroomMixin, UpdateView):
    fields = [
        'name',
        'is_archived',
    ]
    model = Classroom

    def get_queryset(self):
        return self.model.objects.filter(creator=self.request.user)

    def get_success_url(self):
        return self.object.get_detail_url()

    def get_back_url(self):
        return self.object.get_detail_url()
