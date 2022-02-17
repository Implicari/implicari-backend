from django.forms import ModelForm
from django.contrib.auth import get_user_model


User = get_user_model()


class ParentForm(ModelForm):

    class Meta:
        model = User
        fields = (
            'email',
        )

    def __init__(self, *args, **kwargs):
        super(ParentForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True
