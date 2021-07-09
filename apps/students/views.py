from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView

from classrooms.models import Classroom
from classrooms.views import ClassroomMixin

from persons.models import Person

from .forms import StudentForm


User = get_user_model()


class StudentMixin(ClassroomMixin):

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not (
            self.classroom.creator == user or
            self.classroom.students.filter(id=user.id).exists() or
            self.classroom.students.filter(parents=user).exists()
        ):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

    @cached_property
    def classroom(self):
        pk = self.kwargs.get('classroom_pk')
        return get_object_or_404(Classroom, pk=pk)

    def get_context_data(self, *args, **kwargs):
        context = super(StudentMixin, self).get_context_data(*args, **kwargs)

        context['classroom'] = self.classroom
        context['back_url'] = self.get_back_url()

        return context

    def get_queryset(self):
        return self.get_queryset_student()

    def get_queryset_student(self):
        return self.model.objects.filter(classrooms=self.classroom)

    def get_back_url(self):
        raise NotImplementedError


class StudentCreateView(LoginRequiredMixin, StudentMixin, CreateView):
    context_object_name = 'student'
    form_class = StudentForm
    model = Person
    template_name = 'students/student_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        form.instance.classrooms.add(self.classroom)

        email: str = form.cleaned_data['email']
        
        user, _ = User.objects.get_or_create(
            email=email,
            defaults={
                'person': form.instance,
            },
        )

        return response

    def get_success_url(self):
        return reverse('student-detail', kwargs={
            'classroom_pk': self.classroom.id,
            'pk': self.object.id,
        })

    def get_back_url(self):
        return self.classroom.get_student_list_url()


class StudentDeleteView(LoginRequiredMixin, StudentMixin, DeleteView):
    context_object_name = 'student'
    model = Person
    template_name = 'students/student_confirm_delete.html'

    def get_success_url(self):
        return self.classroom.get_student_list_url()

    def get_back_url(self):
        return reverse('student-detail', kwargs={
            'classroom_pk': self.classroom.id,
            'pk': self.object.id,
        })


class StudentDetailView(LoginRequiredMixin, StudentMixin, DetailView):
    context_object_name = 'student'
    model = Person
    template_name = 'students/student_detail.html'

    def get_back_url(self):
        return self.classroom.get_absolute_url()


class StudentUpdateView(LoginRequiredMixin, StudentMixin, UpdateView):
    context_object_name = 'student'
    form_class = StudentForm
    model = Person
    template_name = 'students/student_form.html'

    def get_success_url(self):
        return reverse('student-detail', kwargs={
            'classroom_pk': self.classroom.id,
            'pk': self.object.id,
        })

    def get_back_url(self):
        return reverse('student-detail', kwargs={
            'classroom_pk': self.classroom.id,
            'pk': self.object.id,
        })
