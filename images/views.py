from rest_framework import viewsets
from rest_framework import permissions

from . import models
from . import serializers


class ImageViewSet(viewsets.ModelViewSet):
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer
    permission_classes = []
