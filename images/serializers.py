from rest_framework import serializers

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


class LabelSerializer(serializers.ModelSerializer):
    shape = ShapeField()

    def get_fields(self):
        base_fields = super().get_fields()

        label_format = self.context['request'].query_params.get('format', 'external')

        if label_format == 'internal':
            return base_fields
        else:
            base_fields.pop('shape')
            base_fields['surface'] = serializers.CharField(source='get_surface_as_str')
            return base_fields


    class Meta:
        model = models.Label
        fields = [
            'id',
            'class_id',
            'surface',
            'shape',
        ]


class AnnotationSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True)

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
