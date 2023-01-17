from django import forms
from django.contrib import admin

from django_better_admin_arrayfield.models.fields import ArrayField
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django_better_admin_arrayfield.forms.widgets import DynamicArrayWidget

from .models import Post


class DynamicArrayFileWidget(DynamicArrayWidget):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("subwidget_form", forms.FileInput)
        super().__init__(*args, **kwargs)




class PostAdmin(admin.ModelAdmin, DynamicArrayMixin):
    formfield_overrides = {
        ArrayField: {'widget': DynamicArrayFileWidget},
    }


admin.site.register(Post, PostAdmin)
