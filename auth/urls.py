from django.urls import path

from auth.api import (LoginAPI, ProfileView, RegisterAPI, RequestPasswordReset,
                      ResetPassword)

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('request-password-reset/', RequestPasswordReset.as_view()),
    path('reset-password/<str:token>/', ResetPassword.as_view()),
    path('profile/', ProfileView.as_view(), name='profile'),
]
