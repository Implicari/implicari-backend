from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.utils.functional import cached_property

from classrooms.models import Classroom

from .models import Answer
from .models import Question


class QuestionMixin:

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
        context = super(QuestionMixin, self).get_context_data(*args, **kwargs)

        context['classroom'] = self.classroom

        return context

    def get_queryset(self):
        return self.model.objects.filter(classroom=self.classroom)


class QuestionCreateView(LoginRequiredMixin, QuestionMixin, CreateView):
    model = Question
    fields = [
        'subject',
        'message',
    ]

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.classroom = self.classroom

        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_detail_url()


class QuestionListView(LoginRequiredMixin, QuestionMixin, ListView):
    context_object_name = 'questions'
    model = Question

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('creator').order_by('-creation_timestamp')


class AnswerMixin:

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

    @cached_property
    def question(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Question, pk=pk)

    def get_context_data(self, *args, **kwargs):
        context = super(AnswerMixin, self).get_context_data(*args, **kwargs)

        context['classroom'] = self.classroom
        context['question'] = self.question

        return context


class QuestionDetailView(LoginRequiredMixin, AnswerMixin, CreateView):
    model = Answer
    fields = [
        'message',
    ]
    template_name = 'answers/answer_form.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.question = self.question

        return super().form_valid(form)

    def get_success_url(self):
        return self.question.get_detail_url()
