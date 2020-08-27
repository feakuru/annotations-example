from django.contrib import admin

from . import models

admin.site.register(models.Image)
admin.site.register(models.Annotation)
admin.site.register(models.Label)
