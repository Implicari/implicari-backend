from django.contrib.auth import get_user_model


Domain = get_user_model()


class SignupForm():

    class Meta:
        model = Domain
        fields = (
            'domain',
        )

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields['domain'].required = True
