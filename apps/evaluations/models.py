from django.db import models

from django_pgviews import view as pg

from classrooms.models import Classroom
from persons.models import Person


def get_default_order(*args, **kwargs):
    breakpoint()
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

        if self.classroom:
            evaluation_last = self.classroom.evaluations.last()

            if evaluation_last:
                self.order = evaluation_last.order + 1

            else:
                self.order = 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


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


class DeliveryStatus(pg.View):
    id = models.AutoField(primary_key=True)

    evaluation = models.ForeignKey(
        to=Evaluation,
        related_name='deliveries_status',
        on_delete=models.CASCADE,
    )

    student = models.ForeignKey(
            to=Person,
        related_name='deliveries_status',
        on_delete=models.CASCADE,
    )

    is_delivered = models.BooleanField()

    sql = DELIVERY_STATUS_SQL

    class Meta:
        managed = False
