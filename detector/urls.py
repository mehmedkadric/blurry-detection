from django.urls import path
from django.http import HttpResponse
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "detector"

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('upload/success/', lambda request: HttpResponse('Upload successful!'), name='upload_success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
