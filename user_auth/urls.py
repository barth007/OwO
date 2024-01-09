# USER AUTH URLS MODULE

from django.urls import path
from user_auth import views
from user_auth import kyc_views

app_name = "user_auth"

urlpatterns = [
    path("sign-up/", views.register_view, name="sign-up"),
    path("sign-in/", views.login_view, name="sign-in"),
    path("sign-out/", views.logout_view, name="sign-out"),
    path("kyc/", kyc_views.submit_kyc, name="submit-kyc"),
]