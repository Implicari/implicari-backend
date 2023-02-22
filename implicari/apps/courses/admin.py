from django.contrib import admin

from implicari.apps.persons.models import Student

from .models import Course


class StudentAdminInline(admin.TabularInline):
    model = Student
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    inlines = (
        StudentAdminInline,
    )

    list_display = (
        'id',
        'name',
        'teacher',
    )
