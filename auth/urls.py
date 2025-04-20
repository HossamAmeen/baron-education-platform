from django.urls import path

from auth.api import (
    LoginAPI,
    RegisterAPI,
    RequestPasswordReset,
    ResetPassword,
    StudentProfileView,
)

urlpatterns = [
    path("register/", RegisterAPI.as_view(), name="register"),
    path("login/", LoginAPI.as_view(), name="login"),
    path("request-password-reset/", RequestPasswordReset.as_view()),
    path("reset-password/<str:token>/", ResetPassword.as_view()),
    path("profile/", StudentProfileView.as_view(), name="profile"),
]
