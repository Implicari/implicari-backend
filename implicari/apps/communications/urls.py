from django.urls import path

from .views import MessageCreateView, MessageDetailView, MessageListView


urlpatterns = [
    path('courses/<course_id>/messages/', MessageListView.as_view()),
    path('courses/<course_id>/messages/create/', MessageCreateView.as_view()),
    path('messages/<pk>/', MessageDetailView.as_view()),
]
