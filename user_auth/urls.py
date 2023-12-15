# USER AUTH URLS MODULE

from django.urls import path
from user_auth import views

app_name = "user_auth"

urlpatterns = [
    path("sign-up/", views.register_view, name="sign-up"),
]