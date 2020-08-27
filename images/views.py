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
            if image.annotation is not None:
                return Response(
                    serializers.AnnotationSerializer(
                        image.annotation,
                        context={'request': request}
                    ).data
                )
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = serializers.AnnotationSerializer(
                data=request.data,
                context={'request': request}
            )
            if serializer.is_valid():
                image.annotation.delete()
                image.annotation = serializer.save()
                return Response(serializer.data)
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
