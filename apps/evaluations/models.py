from django.db import models
from django.urls import reverse

from classrooms.models import Classroom
from persons.models import Person


def get_default_order(*args, **kwargs):
    return 1


class Evaluation(models.Model):
    id = models.AutoField(primary_key=True)

    classroom = models.ForeignKey(
        to=Classroom,
        related_name='evaluations',
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = [
            'order',
        ]

    def save(self, *args, **kwargs):

        if self.classroom and self.order is None:
            evaluation_last = self.classroom.evaluations.last()

            if evaluation_last:
                self.order = evaluation_last.order + 1

            else:
                self.order = 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.get_detail_url()

    def get_detail_url(self):
        return reverse('evaluation-detail', kwargs={'pk': self.pk, 'classroom_pk': self.classroom_id})

 

class Delivery(models.Model):
    id = models.AutoField(primary_key=True)

    evaluation = models.ForeignKey(
        to=Evaluation,
        related_name='deliveries',
        on_delete=models.CASCADE,
    )

    student = models.ForeignKey(
        to=Person,
        related_name='deliveries',
        on_delete=models.CASCADE,
    )


DELIVERY_STATUS_SQL = """
    SELECT
        E.id AS id,
        E.id AS evaluation_id,
        P.id AS student_id,
        CASE
            WHEN D.id IS NULL THEN False
            ELSE TRUE
        END
        AS is_delivered

    FROM evaluations_evaluation E

    INNER JOIN classrooms_classroom_students CS ON (CS.classroom_id = E.classroom_id)
    INNER JOIN persons_person P ON (P.id = CS.person_id)
    LEFT JOIN evaluations_delivery D ON (D.evaluation_id = E.id AND D.student_id = P.id)
"""


class Question(models.Model):
    id = models.AutoField(primary_key=True)

    evaluation = models.ForeignKey(
        to=Evaluation,
        related_name='questions',
        on_delete=models.CASCADE,
    )

    statement = models.TextField()


class Alternative(models.Model):
    id = models.AutoField(primary_key=True)

    question = models.ForeignKey(
        to=Question,
        related_name='alternatives',
        on_delete=models.CASCADE,
    )

    text = models.TextField()

    is_correct = models.BooleanField(default=False)
