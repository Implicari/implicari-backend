from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.utils.functional import cached_property

from classrooms.models import Classroom

from .forms import AlternativeForm, AlternativeFormSet, EvaluationForm, QuestionForm
from .models import Alternative, Evaluation, Question


class EvaluationMixin:

    @cached_property
    def classroom(self):
        pk = self.kwargs.get('classroom_pk')
        return get_object_or_404(Classroom, pk=pk, creator=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['classroom'] = self.classroom

        return context

    def get_queryset(self):
        return self.model.objects.filter(classroom=self.classroom)


class EvaluationCreateView(LoginRequiredMixin, EvaluationMixin, CreateView):
    model = Evaluation
    fields = [
        'name',
    ]

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.classroom = self.classroom

        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_list_url()


class EvaluationDeleteView(LoginRequiredMixin, EvaluationMixin, DeleteView):
    model = Evaluation

    def get_success_url(self):
        return self.object.get_list_url()


class EvaluationDetailView(LoginRequiredMixin, EvaluationMixin, DetailView):
    model = Evaluation


class EvaluationUpdateView(LoginRequiredMixin, EvaluationMixin, UpdateView):
    form_class = EvaluationForm
    model = Evaluation

    def get_formset_nested(self):
        return inlineformset_factory(
            parent_model=Question,
            model=Alternative,
            form=AlternativeForm,
            extra=0,
        )


    def get_formset(self):
        return inlineformset_factory(
            parent_model=Evaluation,
            model=Question,
            form=QuestionForm,
            extra=0,
        )

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        result = super().form_valid(form)

        # breakpoint()

        QuestionFormSet = self.get_formset()

        questions_formset = QuestionFormSet(
            form.data,
            instance=self.object,
            prefix='questions_formset',
        )

        if questions_formset.is_valid():
            questions = questions_formset.save()

        AlternativeFormSet = self.get_formset_nested()

        for i, question in enumerate(self.object.questions.all()):
            alternatives_formset = AlternativeFormSet(
                form.data,
                instance=question,
                prefix=f'alternatives_formset_{i}',
            )

            if alternatives_formset.is_valid():
                alternatives_formset.save()


        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        QuestionFormSet = self.get_formset()
        AlternativeFormSet = self.get_formset_nested()

        questions_formset = QuestionFormSet(
            prefix='questions_formset',
            instance=self.object,
        )

        for i, form in enumerate(questions_formset.forms):
            form.formset = AlternativeFormSet(
                prefix=f'alternatives_formset_{i}',
                instance=form.instance,
            )

        context['questions_formset'] = questions_formset

        return context
