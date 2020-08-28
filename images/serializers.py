from rest_framework import serializers
from django.core import validators

from . import models


class ShapeField(serializers.Field):
    """
    Shape objects are serialized into dict notation.
    """

    def to_representation(self, value):
        return {
            'endX': value[0],
            'endY': value[1],
            'startX': value[2],
            'startY': value[3]
        }

    def to_internal_value(self, data):
        return [
            data['endX'],
            data['endY'],
            data['startX'],
            data['startY'],
        ]


class LabelMetaSerializer(serializers.ModelSerializer):
    confidence_percent = serializers.FloatField(
        validators=[
            validators.MinValueValidator(
                0.00,
                "Percent should not be less than zero"
            ),
            validators.MaxValueValidator(
                1,
                "Percent should not be greater than 1"
            ),
        ]
    )

    class Meta:
        model = models.LabelMeta
        fields = [
            'confirmed',
            'confidence_percent'
        ]


class LabelSerializer(serializers.ModelSerializer):
    shape = ShapeField()
    meta = LabelMetaSerializer()

    def get_fields(self):
        base_fields = super().get_fields()

        label_format = self.context['request'].query_params.get('format', 'external')

        if label_format == 'internal':
            return base_fields
        else:
            base_fields.pop('meta')
            base_fields.pop('shape')
            base_fields['surface'] = serializers.CharField(source='get_surface_as_str')
            return base_fields


    class Meta:
        model = models.Label
        fields = [
            'meta',
            'id',
            'class_id',
            'surface',
            'shape',
        ]


class AnnotationSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField('get_labels')
    
    def get_labels(self, obj):
        label_format = self.context['request'].query_params.get('format', 'external')
        if label_format == 'internal':
            return LabelSerializer(
                obj.labels.all(),
                many=True,
                context=self.context,
            ).data
        else:
            return LabelSerializer(
                obj.labels.filter(meta__confirmed=True),
                many=True,
                context=self.context,
            ).data

    class Meta:
        model = models.Annotation
        fields = [
            'labels',
        ]

class ImageSerializer(serializers.ModelSerializer):
    annotation = AnnotationSerializer(required=False)
    class Meta:
        model = models.Image
        fields = [
            'id',
            'image',
            'annotation',
        ]
