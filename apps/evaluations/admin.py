from django.contrib import admin

from evaluations.models import Evaluation
from evaluations.models import Delivery
from evaluations.models import Alternative
from evaluations.models import Question


class AlternativeInline(admin.TabularInline):
    model = Alternative


class QuestionInline(admin.TabularInline):
    model = Question
    inline = (
        AlternativeInline,
    )


class EvaluationAdmin(admin.ModelAdmin):
    fields = (
        'classroom',
        'name',
        'order',
    )

    list_display = (
        'order',
        'name',
    )

    inlines = (
        QuestionInline,
    )


admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(Delivery)
