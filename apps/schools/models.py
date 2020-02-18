from django.db import models

from django_tenants.models import DomainMixin
from django_tenants.models import TenantMixin


class School(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    auto_create_schema = True


class Domain(DomainMixin):
    pass
