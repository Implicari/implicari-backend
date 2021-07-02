from django.contrib import admin
from django.db.models import Count

from .models import Person


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'is_student',
        'is_teacher',
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        queryset = queryset.annotate(
            is_student=Count('classrooms'),
        )

        return queryset

    def is_student(self, obj):
        return obj.is_student

    is_student.boolean = True

    def is_teacher(self, obj):
        return False

    is_teacher.boolean = True


admin.site.register(Person, PersonAdmin)
