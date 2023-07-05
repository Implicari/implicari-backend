from django.contrib import admin

from .models import Student
from .models import Parent


class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'course',
    )


class ParentAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'user',
    )


admin.site.register(Student, StudentAdmin)
admin.site.register(Parent, ParentAdmin)
