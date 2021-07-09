from django.contrib import admin

from evaluations.models import Evaluation
from evaluations.models import Delivery


admin.site.register(Evaluation)
admin.site.register(Delivery)
