from django.contrib import admin

from .models import Question
from .models import Answer


class QuestionAdmin(admin.ModelAdmin):
    pass


class AnswerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
