from rest_framework import serializers

from . import models


class ExternalLabelSerializer(serializers.ModelSerializer):
    surface = serializers.CharField(source='get_surface_as_str')

    class Meta:
        model = models.Label
        fields = [
            'id',
            'class_id',
            'surface',
        ]


class InternalLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Label
        fields = [
            'id',
            'class_id',
            'surface',
            'shape',
        ]


class AnnotationSerializer(serializers.ModelSerializer):
    def __init__(self, labels_format='external', *args, **kwargs):
        if labels_format == 'external':
            self.labels = serializers.ListField(child=ExternalLabelSerializer())
        else:
            self.labels = serializers.ListField(child=InternalLabelSerializer())
        return super(AnnotationSerializer, self).__init__(*args, **kwargs)

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
            'image',
            'annotation',
        ]
