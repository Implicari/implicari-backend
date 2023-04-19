from django.urls import path

from .views import EventCancelView, EventCreateView, EventUpcomingView
from .views import EventDetailView
from .views import EventListView
from .views import EventUpdateView


prefix = 'courses/<int:course_id>/events'


urlpatterns = [
    path(f'{prefix}/', EventListView.as_view()),
    path(f'{prefix}/upcoming/', EventUpcomingView.as_view()),
    path(f'{prefix}/create/', EventCreateView.as_view()),
    path(f'{prefix}/<int:pk>/', EventDetailView.as_view()),
    path(f'{prefix}/<int:pk>/edit/', EventUpdateView.as_view()),
    path(f'{prefix}/<int:pk>/cancel/', EventCancelView.as_view()),
]
