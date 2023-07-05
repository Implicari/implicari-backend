from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'course',
        'sender',
        'is_email_sent',
        'created_at',
    )

    list_filter = (
        'course',
        'sender',
        'is_email_sent',
        'created_at',
    )