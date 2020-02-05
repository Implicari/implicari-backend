from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.utils.functional import cached_property

from classrooms.models import Classroom

from .models import Event


class EventMixin:

    @cached_property
    def classroom(self):
        pk = self.kwargs.get('classroom_pk')
        return get_object_or_404(Classroom, pk=pk, creator=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(EventMixin, self).get_context_data(*args, **kwargs)

        context['classroom'] = self.classroom

        return context

    def get_queryset(self):
        return self.model.objects.filter(classroom=self.classroom)


class EventCreateView(LoginRequiredMixin, EventMixin, CreateView):
    model = Event
    fields = [
        'description',
        'date',
        'message',
    ]

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.classroom = self.classroom

        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_list_url()


class EventDeleteView(LoginRequiredMixin, EventMixin, DeleteView):
    model = Event

    def get_success_url(self):
        return self.object.get_list_url()


class EventDetailView(LoginRequiredMixin, EventMixin, DetailView):
    model = Event


class EventListView(LoginRequiredMixin, EventMixin, ListView):
    context_object_name = 'events'
    model = Event

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('creator').order_by('-creation_timestamp')


class EventUpdateView(LoginRequiredMixin, EventMixin, UpdateView):
    fields = [
        'description',
        'date',
        'message',
    ]
    model = Event

    def get_success_url(self):
        return self.object.get_list_url()
