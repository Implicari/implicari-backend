from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class UserCreationForm(BaseUserCreationForm):

    class Meta:
        model = User
        fields = (
            User.USERNAME_FIELD,
        )

    # def __init__(self, *args, **kwargs):
    #     super(UserCreationForm, self).__init__(*args, **kwargs)

    #     self.fields['email'].required = True
