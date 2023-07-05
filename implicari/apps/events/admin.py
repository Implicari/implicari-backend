from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'description',
        'course',
        'date',
        'time',
    )

    list_editable = (
        'name',
        'description',
        'course',
        'date',
        'time',
    )
