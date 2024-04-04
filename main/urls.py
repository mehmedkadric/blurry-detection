from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("profile/<int:user_id>/", views.profile, name="profile"),
    path("edit/<int:user_id>/", views.update_user, name="edit"),
    path('change-password/', views.change_password, name='change_password'),

]