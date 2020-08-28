import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField


class Image(models.Model):
    """
    An annotated Image.
    """
    image = models.ImageField()
    annotation = models.OneToOneField(
        'images.Annotation',
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )


class Annotation(models.Model):
    """
    An Annotation for an Image consisting of multiple labels.
    """
    labels = models.ManyToManyField(
        'images.Label',
        blank=True,
    )


LABEL_CLASS_ID_CHOICES = ('tooth', 'gum', 'lip')

class Label(models.Model):
    """
    A Label containing some example ML model info.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    class_id = models.TextField(
        choices=[(item, item) for item in LABEL_CLASS_ID_CHOICES],
    )
    surface = ArrayField(
        models.CharField(max_length=1),
        null=True,
        blank=True,
    )
    shape = ArrayField(
        models.FloatField(), size=4,
        null=True,
        blank=True,
    )

    def get_surface_as_str(self):
        """Return `surface` as a joined string."""
        return ''.join(elt for elt in self.surface)


class LabelMeta(models.Model):
    """
    Meta info on a Label
    representing if it is confirmed
    and how confident we are about it.
    """
    label = models.OneToOneField('Label', related_name='meta', on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    confidence_percent = models.FloatField()
