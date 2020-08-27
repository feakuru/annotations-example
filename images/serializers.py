from rest_framework import serializers

from . import models


class ExternalLabelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Label
        fields = [
            'id',
            'class_id',
            'surface',
        ]


class LabelSerializer(serializers.ModelSerializer):

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
