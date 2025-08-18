from django.urls import path

from auth.api import (
    LoginAPI,
    RegisterAPI,
    RequestPasswordReset,
    StudentProfileView,
)
from auth.views import PasswordResetConfirmView

urlpatterns = [
    path("register/", RegisterAPI.as_view(), name="register"),
    path("login/", LoginAPI.as_view(), name="login"),
    path("request-password-reset/", RequestPasswordReset.as_view()),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("profile/", StudentProfileView.as_view(), name="profile"),
]
