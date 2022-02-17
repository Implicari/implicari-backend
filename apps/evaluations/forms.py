from django.forms import ModelForm
from django.forms import widgets
from django.forms.models import inlineformset_factory
from django.forms.widgets import Input, Textarea

from .models import Evaluation
from .models import Question
from .models import Alternative


class AlternativeForm(ModelForm):

    class Meta:
        model = Alternative
        fields = '__all__'
        widgets = {
            'text': Input(),
        }


class QuestionForm(ModelForm):

    class Meta:
        model = Question
        fields = '__all__'
        widgets = {
            'statement': Textarea(attrs={'rows': 2}),
        }


class EvaluationForm(ModelForm):

    class Meta:
        model = Evaluation
        fields = '__all__'


AlternativeFormSet = inlineformset_factory(
    parent_model=Question,
    model=Alternative,
    form=AlternativeForm,
    extra=1,
)


QuestionFormSet = inlineformset_factory(
    parent_model=Evaluation,
    model=Question,
    form=QuestionForm,
    extra=1,
)
