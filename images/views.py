from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models
from . import serializers


class ImageViewSet(viewsets.ModelViewSet):
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer
    permission_classes = []

    @action(detail=True, methods=['get', 'post'])
    def annotation(self, request, pk):
        image = self.get_object()
        if request.method == 'GET':
            return Response(
                serializers.AnnotationSerializer(image.annotation).data
            )
        else:
            serializer = serializers.AnnotationSerializer(data=request.data)
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
