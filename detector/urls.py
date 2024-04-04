from django.urls import path
from . import views

app_name = "detector"

urlpatterns = [
    path("detect/", views.detect, name="detect"),
]
