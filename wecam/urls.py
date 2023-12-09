from django.urls import path
from .views import process_image
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', process_image , name='process_image'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)