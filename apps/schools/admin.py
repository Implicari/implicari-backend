from django.contrib import admin

from django_tenants.admin import TenantAdminMixin

from .models import School


@admin.register(School)
class SchoolAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'created_on', 'updated_on')
