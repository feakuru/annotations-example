from django.contrib import admin
from django.urls import path, include
from images import urls as images_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(images_urls.router.urls)),
]
