import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField


class Image(models.Model):
    image = models.ImageField()
    annotation = models.OneToOneField(
        'images.Annotation',
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )


class Annotation(models.Model):
    labels = models.ManyToManyField(
        'images.Label',
        blank=True,
    )


LABEL_CLASS_ID_CHOICES = ('tooth', 'gum', 'lip')

class Label(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    class_id = models.TextField(
        choices=[(item, item) for item in LABEL_CLASS_ID_CHOICES],
    )
    surface = ArrayField(models.CharField(max_length=1))
    shape = ArrayField(models.FloatField(), size=4)
