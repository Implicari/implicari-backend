from django.db import models


class School(models.Model):
    name = models.CharField(max_length=100)

    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
