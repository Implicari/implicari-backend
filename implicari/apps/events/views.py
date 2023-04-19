from datetime import date
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView

from .models import Event
from .serializers import (
    EventCancelSerializer,
    EventCreateSerializer,
    EventListSerializer,
    EventUpdateSerializer,
)


class EventListView(ListAPIView):
    serializer_class = EventListSerializer
    queryset = Event.objects.all()

    def get_queryset(self):
        return self.queryset.filter(course=self.kwargs['course_id'])


class EventUpcomingView(EventListView):
    def get_queryset(self):
        return super().get_queryset().filter(date__gte=date.today())


class EventDetailView(ListAPIView):
    serializer_class = EventListSerializer
    queryset = Event.objects.all()

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])


class EventCreateView(CreateAPIView):
    serializer_class = EventCreateSerializer
    queryset = Event.objects.all()

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user,
            course_id=self.kwargs['course_id'],
        )


class EventUpdateView(UpdateAPIView):
    serializer_class = EventUpdateSerializer
    queryset = Event.objects.all()


class EventCancelView(UpdateAPIView):
    serializer_class = EventCancelSerializer
    queryset = Event.objects.all()

    def perform_update(self, serializer):
        serializer.save(canceled=True)