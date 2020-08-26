from rest_framework import serializers

from . import models


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Image
        fields = ['image', 'annotation']
