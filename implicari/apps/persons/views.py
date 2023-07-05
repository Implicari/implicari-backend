from django.db.models import Q

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from .models import Parent, Student
from .serializers import ParentSerializer, StudentSerializer


class StudentList(ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Student.objects.distinct().filter(course=self.kwargs['course_id']).filter(Q(course__teacher=self.request.user) | Q(parents__user=self.request.user))


class StudentCreate(CreateAPIView):
    serializer_class = StudentSerializer

    def perform_create(self, serializer):
        serializer.save(course_id=self.kwargs['course_id'])


class StudentDetail(RetrieveAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Student.objects.distinct().filter(
            Q(parents__user=self.request.user) | Q(course__teacher=self.request.user)
        )


class ParentList(ListAPIView):
    serializer_class = ParentSerializer

    def get_queryset(self):
        return Parent.objects.filter(students=self.kwargs['student_id'])
    

class ParentCreate(CreateAPIView):
    serializer_class = ParentSerializer

    def perform_create(self, serializer):
        serializer.save(student_id=self.kwargs['student_id'])


class ParentDetail(RetrieveAPIView):
    serializer_class = ParentSerializer

    def get_queryset(self):
        return Parent.objects.distinct().filter(students__course__teacher=self.request.user)
