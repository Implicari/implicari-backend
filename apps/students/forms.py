from django import forms
from django.forms import ModelForm

from persons.models import Person


class StudentForm(ModelForm):

    email = forms.EmailField(required=False)

    class Meta:
        model = Person
        fields = [
            'first_name',
            'last_name',
            'run',
        ]
