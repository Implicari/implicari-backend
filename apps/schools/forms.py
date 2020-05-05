# from django.contrib.auth import get_user_model
from django.forms import ModelForm

from .models import Domain

# Domain = get_user_model()


class SigninForm(ModelForm):

    class Meta:
        model = Domain
        fields = (
            'domain',
        )

    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)

        self.fields['domain'].required = True
