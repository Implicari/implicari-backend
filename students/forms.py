from django.forms import ModelForm
from django.contrib.auth import get_user_model


User = get_user_model()


class StudentForm(ModelForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
        )

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
