from django.forms import ModelForm

from persons.models import Person


class StudentForm(ModelForm):

    class Meta:
        model = Person
        fields = [
            'first_name',
            'last_name',
            'run',
        ]
