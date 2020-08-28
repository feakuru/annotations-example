from rest_framework import serializers
from drf_base64 import fields as base64_fields
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
    """
    Serializer validating that confidence_percent is in the [0, 1] range.
    """
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
    """Serializer for Label that works in both internal and external formats."""
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
            base_fields['surface'] = serializers.CharField(
                source='get_surface_as_str',
            )
            return base_fields
    
    def create(self, validated_data):
        meta_data = validated_data.pop(
            'meta',
            {
                'confirmed': False,
                'confidence_percent': 0.00
            }
        )
        if 'get_surface_as_str' in validated_data:
            validated_data['surface'] = list(validated_data.pop('get_surface_as_str'))
        label = models.Label.objects.create(**validated_data)
        models.LabelMeta.objects.create(label=label, **meta_data)
        return label


    class Meta:
        model = models.Label
        fields = [
            'meta',
            'id',
            'class_id',
            'surface',
            'shape',
        ]


class LabelsField(serializers.Field):
    """
    Field that filters labels based on context and formats based on format.
    """

    def to_representation(self, value):
        label_format = self.context['request'].query_params.get(
            'format',
            'external'
        )
        if label_format == 'internal':
            return LabelSerializer(
                value,
                many=True,
                context=self.context,
            ).data
        else:
            return LabelSerializer(
                value.filter(meta__confirmed=True),
                many=True,
                context=self.context,
            ).data

    def to_internal_value(self, data):
        serializer = LabelSerializer(
            data=data,
            many=True,
            context=self.context,
        )
        if serializer.is_valid():
            labels = serializer.save()
            return labels
        else:
            raise serializers.ValidationError(serializer.errors)


class AnnotationSerializer(serializers.ModelSerializer):
    """Annotation serializer that handles the labels MTM field."""
    labels = LabelsField()

    def create(self, validated_data):
        labels = validated_data.pop('labels')
        annotation = models.Annotation.objects.create(**validated_data)
        for label in labels:
            annotation.labels.add(label)
        return annotation

    class Meta:
        model = models.Annotation
        fields = [
            'labels',
        ]

class ImageSerializer(serializers.ModelSerializer):
    """Serializer for an Image that creates an annotation if provided."""
    image = base64_fields.Base64ImageField()
    annotation = AnnotationSerializer(required=False)

    def create(self, validated_data):
        image = models.Image.objects.create(image=validated_data['image'])
        annotation_data = validated_data.get('annotation', {})
        if annotation_data:
            image.annotation = models.Annotation.objects.create()
            image.annotation.labels.set(annotation_data.get('labels', []))
            image.annotation.save()
            image.save()
        return image


    class Meta:
        model = models.Image
        fields = [
            'id',
            'image',
            'annotation',
        ]
