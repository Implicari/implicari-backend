from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from .serializers import MessageCreateSerializer, MessageDetailSerializer, MessageListSerializer
from .models import Message


class MessageListView(ListAPIView):
    serializer_class = MessageListSerializer

    def get_queryset(self):
        return Message.objects.filter(course=self.kwargs['course_id'])
    

class MessageDetailView(RetrieveAPIView):
    serializer_class = MessageDetailSerializer

    def get_queryset(self):
        return Message.objects.filter(course=self.kwargs['course_id'])
    

class MessageCreateView(CreateAPIView):
    serializer_class = MessageCreateSerializer

    def get_queryset(self):
        return Message.objects.filter(course=self.kwargs['course_id'])

    def perform_create(self, serializer):
        serializer.save(course_id=self.kwargs['course_id'], sender=self.request.user)