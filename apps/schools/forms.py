from django.forms import Form
from django.forms.fields import SlugField


class SigninForm(Form):
    subdomain = SlugField(required=True)
