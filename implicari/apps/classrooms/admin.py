from django.contrib import admin
from django.db.models import Count

from .models import Classroom


class ClassroomAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'creator',
        # 'students_count',
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        # queryset = queryset.annotate(
        #     students_count=Count('students'),
        # )

        return queryset

    def students_count(self, obj):
        return obj.students_count


admin.site.register(Classroom, ClassroomAdmin)
