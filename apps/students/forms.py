from typing import Any
from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from persons.models import Person


User = get_user_model()


class StudentForm(ModelForm):

    email = forms.EmailField(required=False)

    class Meta:
        model = Person
        fields = [
            'first_name',
            'last_name',
        ]

    def save(self, commit: bool=True) -> Any:
        instance = super().save(commit=False)

        email = self.cleaned_data['email']

        user, _ = User.objects.get_or_create(email=email)

        instance.user = user

        if commit:
            instance.save()

        return instance
