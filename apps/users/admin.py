from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'avatar',
        'first_name',
        'last_name',
        'is_active',
    ]


admin.site.register(User, UserAdmin)
