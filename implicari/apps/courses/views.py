from rest_framework.generics import ListAPIView

from implicari.utils.classes import StandardPagination

from .serializers import CourseSerializer
from .models import Course


class CourseList(ListAPIView):

    pagination_class = StandardPagination
    queryset = Course.objects.all()
    search_fields = (
        'name',
    )
    serializer_class = CourseSerializer

    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)
