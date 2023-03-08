from rest_framework.generics import ListAPIView, RetrieveAPIView

from implicari.utils.classes import StandardPagination

from .serializers import CourseRetriveSerializer, CourseSerializer
from .models import Course


class CourseTeacherList(ListAPIView):

    pagination_class = StandardPagination
    search_fields = (
        'name',
    )
    serializer_class = CourseSerializer

    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)


class CourseParentList(ListAPIView):

    pagination_class = StandardPagination
    search_fields = (
        'name',
    )
    serializer_class = CourseSerializer

    def get_queryset(self):
        return Course.objects.filter(students__parents__user=self.request.user)


class CourseRetrive(RetrieveAPIView):

    queryset = Course.objects.all()
    serializer_class = CourseRetriveSerializer
